# -*- coding: utf-8 -*-
"""
Card Images
===========

Pelican plugin that renders a 1200x630 Open-Graph "title card" PNG for every
published article that does not ship its own lead image, and exposes the card's
URL to the templates as ``article.card_image``.

Why
---
The site's ``BlogPosting.image`` / ``og:image`` were previously missing on
articles (the site-wide default was just the author headshot). These cards fill
that gap with an on-brand share preview, improving Google Discover/SERP
thumbnails and social + AI-assistant previews.

Placement is **share-preview only**: the card is emitted as ``og:image`` /
``twitter:image`` + ``BlogPosting.image`` and is *never* rendered on the article
page (see ``partial/og.html`` and ``partial/jsonld/blogposting.html``).

Two card templates, both on an Ink ground (design mirrors ``site.css``):

* **Post card**  -- category eyebrow, title (auto-fit size tier), byline, domain.
* **Review card** -- adds a score panel (big numeral + "out of 10" + verdict
  badge) and a Provider / Workload meta row. Verdict bands:
  ``>=9`` Highly Recommended, ``>=7`` Recommended, ``>=5.5`` Worth a look
  (amber), else Avoid (muted grey + dimmed panel).

When a card is (not) generated
------------------------------
For each published article:

* ``no_card: true`` in the front matter  -> no card (falls back to the site
  default headshot og:image).
* a ``cover:`` field is set              -> no card; that image is used instead
  (author override; wired through ``og.html`` / ``blogposting.html``).
* otherwise                              -> a card is generated.

Incremental generation
-----------------------
Rendering is deterministic: an input hash (title/category/score/... +
``CARD_VERSION``) is computed per card. If ``CARD_CACHE_DIR`` points at a folder
of previously generated cards + ``cards-manifest.json`` with a matching hash, the
existing PNG is copied instead of re-rendered. The plugin itself only ever
touches the local filesystem -- restoring/persisting the cache across CI runs is
the pipeline's job (see ``deploy.yml``). With no cache dir, every card is simply
rendered (correct for first run and local builds).

Settings (all optional; sensible defaults):
    CARD_GENERATE       bool  master on/off (default True)
    CARD_OUTPUT_DIR     str   output subdir + URL path (default "theme/img/cards")
    CARD_CACHE_DIR      str   folder of prior cards + manifest for incremental
    CARD_VERSION        str   bump to force a full re-render (default "1")
    CARD_FONT_DIR       str   dir with the 4 bundled TTFs (default: ./fonts)
    CARD_LOGO           str   logo PNG (default: THEME/static/img/logo-512.png)
    CARD_HEADSHOT       str   headshot PNG (default: THEME/static/img/wegner_headshot.png)
    CARD_NAME           str   byline name (default: AUTHOR_DISPLAY or AUTHOR)
    CARD_ROLE           str   byline role (default: "Engineering Leadership")
    CARD_DOMAIN         str   footer domain (default: derived from SITEURL)
Reused from existing config: REVIEW_PROVIDERS (provider display name + itemType).

Front-matter fields consumed (all already authored on the posts):
    Category, Title, template (== "review"), revieweditem, score, provider,
    workload (ISO-8601 PTxxHxxM). Optional new: no_card, review_kind.
"""
import hashlib
import json
import logging
import math
import os
import re
import shutil
from html import unescape

from pelican import signals

try:
    from PIL import Image, ImageDraw, ImageFont, ImageChops
except Exception:  # pragma: no cover - Pillow missing -> plugin no-ops
    Image = None

logger = logging.getLogger(__name__)

MANIFEST_NAME = "cards-manifest.json"

# ============================================================ colour system ==
# Cards are authored in OKLCH (matches site.css); Pillow works in sRGB, so
# convert here. color-mix(in oklch, ...) is approximated by mixing in OKLab --
# visually identical for these low-chroma tints and free of the hue-wraparound a
# true polar LCH lerp would hit between rose (h=24) and ink (h=265).

def _oklab_to_lin(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return r, g, bb


def _lin_to_srgb8(x):
    x = max(0.0, min(1.0, x))
    y = 12.92 * x if x <= 0.0031308 else 1.055 * (x ** (1 / 2.4)) - 0.055
    return int(round(max(0.0, min(1.0, y)) * 255))


def _oklch(L, C, h):
    hr = math.radians(h)
    r, g, bb = _oklab_to_lin(L, C * math.cos(hr), C * math.sin(hr))
    return (_lin_to_srgb8(r), _lin_to_srgb8(g), _lin_to_srgb8(bb))


def _oklch_to_oklab(L, C, h):
    hr = math.radians(h)
    return (L, C * math.cos(hr), C * math.sin(hr))


def _mix_oklch(c1, c2, w1):
    L1, a1, b1 = _oklch_to_oklab(*c1)
    L2, a2, b2 = _oklch_to_oklab(*c2)
    w2 = 1.0 - w1
    r, g, bb = _oklab_to_lin(L1 * w1 + L2 * w2, a1 * w1 + a2 * w2, b1 * w1 + b2 * w2)
    return (_lin_to_srgb8(r), _lin_to_srgb8(g), _lin_to_srgb8(bb))


def _over(fg, bg, alpha):
    return tuple(int(round(f * alpha + b * (1 - alpha))) for f, b in zip(fg, bg))


# --- design tokens (OKLCH triples, from the locked mock) ---------------------
T_BG = (0.205, 0.014, 265)
T_INK = (0.96, 0.004, 85)
T_INK_MUT = (0.75, 0.012, 260)
T_INK_FAINT = (0.62, 0.012, 260)
T_ACCENT = (0.66, 0.12, 24)
T_ACCENT_INK = (0.78, 0.11, 26)
T_AMBER = (0.77, 0.09, 82)
T_TITLE = (0.97, 0.01, 40)
T_WHITE = (1.0, 0.0, 89)

BG = _oklch(*T_BG)
INK = _oklch(*T_INK)
INK_MUT = _oklch(*T_INK_MUT)
INK_FAINT = _oklch(*T_INK_FAINT)
ACCENT = _oklch(*T_ACCENT)
ACCENT_INK = _oklch(*T_ACCENT_INK)
AMBER = _oklch(*T_AMBER)
TITLE = _oklch(*T_TITLE)

LINE = _over((255, 255, 255), BG, 0.15)
ACCENT_SOFT = _over(ACCENT, BG, 0.26)
HATCH = _over(ACCENT, BG, 0.10)
EYE_DOT_GLOW = _over(ACCENT, BG, 0.26)
AVATAR_GLOW = _over(ACCENT, BG, 0.22)
PANEL_BG = _mix_oklch(T_ACCENT, T_BG, 0.16)
PANEL_BG_AVOID = _mix_oklch(T_WHITE, T_BG, 0.06)
PANEL_BORDER_AVOID = _mix_oklch(T_INK, T_BG, 0.45)
VERDICT_AVOID_BG = _mix_oklch(T_INK, T_BG, 0.40)
VERDICT_AVOID_FG = _oklch(0.9, 0.004, 85)

CARD_W, CARD_H = 1200, 630
CONTENT_L, CONTENT_R = 84, 1116
CONTENT_W = CONTENT_R - CONTENT_L
SS = 2  # supersample factor (rendered at 2x then downsampled with LANCZOS)

_FONT_FILES = {
    "inter": "Inter-Regular.ttf",
    "inter600": "Inter-SemiBold.ttf",
    "mono": "JetBrainsMono-Regular.ttf",
    "mono600": "JetBrainsMono-SemiBold.ttf",
}


class _Fonts:
    def __init__(self, font_dir, scale=1):
        self.dir, self.scale, self._c = font_dir, scale, {}

    def get(self, family, px):
        key = (family, px)
        if key not in self._c:
            self._c[key] = ImageFont.truetype(
                os.path.join(self.dir, _FONT_FILES[family]), int(round(px * self.scale)))
        return self._c[key]


# ------------------------------------------------------------- text helpers ---
def _tw(draw, text, font, tracking):
    if not text:
        return 0
    w = 0
    for ch in text:
        w += draw.textlength(ch, font=font) + tracking
    return w - tracking


def _draw_tracked(draw, xy, text, font, fill, tracking, anchor="la"):
    x, y = xy
    va = anchor[1]
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill, anchor="l" + va)
        x += draw.textlength(ch, font=font) + tracking


def _center_tracked(draw, cx, y, text, font, fill, tracking, va="a"):
    _draw_tracked(draw, (cx - _tw(draw, text, font, tracking) / 2, y), text, font, fill,
                  tracking, anchor="l" + va)


def _wrap(draw, text, font, tracking, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if not cur or _tw(draw, trial, font, tracking) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def _format_workload(iso):
    if not iso:
        return None
    m = re.match(r"^P(?:T)?(?:(\d+)H)?(?:(\d+)M)?$", str(iso).strip(), re.I)
    if not m:
        return str(iso)
    parts = []
    if m.group(1):
        parts.append("%dh" % int(m.group(1)))
    if m.group(2):
        parts.append("%dm" % int(m.group(2)))
    return " ".join(parts) if parts else None


def _verdict_for(score):
    if score >= 9.0:
        return ("Highly Recommended", "normal")
    if score >= 7.0:
        return ("Recommended", "normal")
    if score >= 5.5:
        return ("Worth a look", "worth")
    return ("Avoid", "avoid")


# ------------------------------------------------------------------ assets ----
def _circle_avatar(path, size):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s)).resize(
        (size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    im.putalpha(mask)
    return im


def _logo_tile(path, tile, glyph, radius):
    base = Image.new("RGBA", (tile, tile), (0, 0, 0, 0))
    m = Image.new("L", (tile, tile), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, tile - 1, tile - 1], radius=radius, fill=255)
    white = Image.new("RGBA", (tile, tile), (252, 251, 249, 255))
    base = Image.composite(white, base, m)
    logo = Image.open(path).convert("RGBA").resize((glyph, glyph), Image.LANCZOS)
    off = (tile - glyph) // 2
    base.alpha_composite(logo, (off, off))
    return base, m


_HATCH_CACHE = {}


def _hatch_layer(S):
    """Faint 135deg accent hatch that fades in from the top-right corner.

    Identical for every card at a given supersample factor, so it is built once
    and reused (read-only paste)."""
    if S in _HATCH_CACHE:
        return _HATCH_CACHE[S]
    W, H = CARD_W * S, CARD_H * S
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    col = HATCH + (255,)
    step = 31 * S
    x = int(W * 0.30)
    while x < W + H:
        ld.line([(x, 0), (x - H, H)], fill=col, width=max(1, S))
        x += step
    mw, mh = 120, 63
    m = Image.new("L", (mw, mh), 0)
    mp = m.load()
    for j in range(mh):
        for i in range(mw):
            t = (1 - i / (mw - 1)) * 0.62 + (j / (mh - 1)) * 0.62
            mp[i, j] = int(max(0.0, 1.0 - t / 0.60) * 95)
    m = m.resize((W, H), Image.BILINEAR)
    layer.putalpha(ImageChops.multiply(layer.getchannel("A"), m))
    _HATCH_CACHE[S] = layer
    return layer


# ================================================================= render ====
def render_card(spec, S=SS):
    """Render a card from ``spec`` and return a 1200x630 RGB PIL image.

    spec keys: kind ('post'|'review'), eyebrow, name, role, domain, logo_path,
    headshot_path, fonts_dir; post -> title; review -> review_kind, item,
    provider, workload, score.
    """
    F = _Fonts(spec["fonts_dir"], scale=S)
    img = Image.new("RGB", (CARD_W * S, CARD_H * S), BG)
    d = ImageDraw.Draw(img, "RGBA")

    hatch = _hatch_layer(S)
    img.paste(hatch, (0, 0), hatch)
    d.rectangle([0, 0, 10 * S, CARD_H * S], fill=ACCENT)  # left rail

    # ---- c-top: eyebrow chip ----
    f_eye = F.get("mono600", 16)
    eye = spec["eyebrow"].upper()
    eye_tr = 0.18 * 16 * S
    ea, ed = f_eye.getmetrics()
    dot, padx, pady, gap = 9 * S, 16 * S, 11 * S, 12 * S
    tw = _tw(d, eye, f_eye, eye_tr)
    chip_h = (ea + ed) + pady * 2 - 4 * S
    chip_w = padx + dot + gap + tw + padx
    cx0, cy0 = 84 * S, 78 * S
    d.rounded_rectangle([cx0, cy0, cx0 + chip_w, cy0 + chip_h], radius=3 * S, fill=ACCENT_SOFT)
    dcx, dcy = cx0 + padx + dot / 2, cy0 + chip_h / 2
    d.ellipse([dcx - dot / 2 - 5 * S, dcy - dot / 2 - 5 * S, dcx + dot / 2 + 5 * S, dcy + dot / 2 + 5 * S],
              fill=EYE_DOT_GLOW)
    d.ellipse([dcx - dot / 2, dcy - dot / 2, dcx + dot / 2, dcy + dot / 2], fill=ACCENT)
    _draw_tracked(d, (cx0 + padx + dot + gap, dcy), eye, f_eye, ACCENT_INK, eye_tr, anchor="lm")

    # ---- logo top-right ----
    tile_dev = 60 * S
    tile, tmask = _logo_tile(spec["logo_path"], tile_dev, 44 * S, 15 * S)
    img.paste(tile, (int(1116 * S - tile_dev), int(78 * S)), tmask)

    # ---- foot geometry ----
    foot_bottom = 562 * S
    avatar = 74 * S
    foot_top = foot_bottom - avatar
    border_y = foot_top - 24 * S
    d.rectangle([84 * S, border_y, 1116 * S, border_y + 2 * S], fill=ACCENT)

    av = _circle_avatar(spec["headshot_path"], int(avatar))
    acx, acy = 84 * S + avatar / 2, foot_top + avatar / 2
    d.ellipse([acx - avatar / 2 - 6 * S, acy - avatar / 2 - 6 * S, acx + avatar / 2 + 6 * S, acy + avatar / 2 + 6 * S],
              fill=AVATAR_GLOW)
    d.ellipse([acx - avatar / 2 - 2 * S, acy - avatar / 2 - 2 * S, acx + avatar / 2 + 2 * S, acy + avatar / 2 + 2 * S],
              fill=ACCENT)
    img.paste(av, (int(84 * S), int(foot_top)), av)

    f_name, f_role = F.get("inter600", 23), F.get("mono", 13)
    na, nd = f_name.getmetrics()
    ra, rd = f_role.getmetrics()
    block_h = (na + nd) + 4 * S + (ra + rd)
    tx = 84 * S + avatar + 20 * S
    by = acy - block_h / 2
    d.text((tx, by), spec["name"], font=f_name, fill=INK, anchor="la")
    _draw_tracked(d, (tx, by + (na + nd) + 4 * S), spec["role"].upper(), f_role, ACCENT_INK, 0.14 * 13 * S)

    f_url = F.get("mono600", 18)
    url_tr, udot = 0.06 * 18 * S, 8 * S
    uw = _tw(d, spec["domain"], f_url, url_tr)
    ux = 1116 * S - (udot + 14 * S + uw)
    d.ellipse([ux, acy - udot / 2, ux + udot, acy + udot / 2], fill=ACCENT)
    _draw_tracked(d, (ux + udot + 14 * S, acy), spec["domain"], f_url, ACCENT_INK, url_tr, anchor="lm")

    body_bottom = border_y - 34 * S
    if spec["kind"] == "post":
        _draw_title(d, spec["title"], F, body_bottom, S)
    else:
        _draw_review(d, spec, F, body_bottom, S)

    if S != 1:
        img = img.resize((CARD_W, CARD_H), Image.LANCZOS)
    return img


def _draw_title(d, title, F, bottom, S):
    tiers = [(80, 1.04, 2), (60, 1.07, 3), (46, 1.12, 4)]
    max_w = (CONTENT_W - 8) * S
    chosen = None
    for px, lh, maxl in tiers:
        f = F.get("inter", px)
        tr = -0.022 * px * S
        lines = _wrap(d, title, f, tr, max_w)
        if len(lines) <= maxl:
            chosen = (f, px, lh, tr, lines)
            break
    if chosen is None:
        px, lh, maxl = tiers[-1]
        f = F.get("inter", px)
        tr = -0.022 * px * S
        chosen = (f, px, lh, tr, _wrap(d, title, f, tr, max_w)[:maxl])
    f, px, lh, tr, lines = chosen
    line_adv = px * lh * S
    asc, desc = f.getmetrics()
    total_h = line_adv * (len(lines) - 1) + (asc + desc)
    y = bottom - total_h
    for ln in lines:
        _draw_tracked(d, (CONTENT_L * S, y), ln, f, TITLE, tr)
        y += line_adv


def _draw_review(d, spec, F, bottom, S):
    score = float(spec["score"])
    verdict, variant = _verdict_for(score)
    is_avoid = variant == "avoid"
    sc_txt = "%g" % round(score, 1)
    f_score, f_outof, f_verd = F.get("inter", 96), F.get("mono", 13), F.get("mono600", 13)
    sa, sd = f_score.getmetrics()
    score_h = sa + sd
    oa, od = f_outof.getmetrics()
    outof_h = oa + od
    va, vd = f_verd.getmetrics()
    outof_txt, outof_tr = "OUT OF 10", 0.2 * 13 * S
    verd_txt, verd_tr = verdict.upper(), 0.12 * 13 * S
    verd_h = (va + vd) + 8 * S * 2
    sw = _tw(d, sc_txt, f_score, 0)
    ow = _tw(d, outof_txt, f_outof, outof_tr)
    bw = _tw(d, verd_txt, f_verd, verd_tr) + 14 * S * 2
    pad = 34 * S
    panel_w = max(220 * S, max(sw, ow, bw) + pad * 2)
    panel_h = 24 * S + score_h + 8 * S + outof_h + 16 * S + verd_h + 24 * S
    px1 = 1116 * S
    px0 = px1 - panel_w
    py1, py0 = bottom, bottom - panel_h
    d.rounded_rectangle([px0, py0, px1, py1], radius=6 * S,
                        fill=(PANEL_BG_AVOID if is_avoid else PANEL_BG), outline=LINE, width=max(1, S))
    d.rounded_rectangle([px0, py0, px0 + 5 * S, py1], radius=3 * S,
                        fill=(PANEL_BORDER_AVOID if is_avoid else ACCENT))
    pcx = (px0 + px1) / 2
    yy = py0 + 24 * S
    _center_tracked(d, pcx, yy, sc_txt, f_score, (INK_MUT if is_avoid else TITLE), 0)
    yy += score_h + 8 * S
    _center_tracked(d, pcx, yy, outof_txt, f_outof, INK_MUT, outof_tr)
    yy += outof_h + 16 * S
    if variant == "avoid":
        bg, fg = VERDICT_AVOID_BG, VERDICT_AVOID_FG
    elif variant == "worth":
        bg, fg = AMBER, BG
    else:
        bg, fg = ACCENT, BG
    bx0 = pcx - bw / 2
    d.rounded_rectangle([bx0, yy, bx0 + bw, yy + verd_h], radius=3 * S, fill=bg)
    _draw_tracked(d, (bx0 + 14 * S, yy + verd_h / 2), verd_txt, f_verd, fg, verd_tr, anchor="lm")

    # ---- left column ----
    left_l = CONTENT_L * S
    left_r = px0 - 44 * S
    left_w = left_r - left_l
    cells = [("PROVIDER", spec.get("provider")), ("WORKLOAD", _format_workload(spec.get("workload")))]
    cells = [(k, v) for k, v in cells if v]
    f_dt, f_dd = F.get("mono", 12), F.get("inter600", 19)
    dt_tr = 0.15 * 12 * S
    dta, dtd = f_dt.getmetrics()
    dt_h = dta + dtd
    dda, ddd = f_dd.getmetrics()
    dd_h = dda + ddd
    cell_h = dt_h + 5 * S + dd_h
    cells_top = bottom - cell_h
    line_y = cells_top - 18 * S
    d.rectangle([left_l, line_y, left_r, line_y + max(1, S)], fill=LINE)
    cxp = left_l
    for k, v in cells:
        _draw_tracked(d, (cxp, cells_top), k, f_dt, INK_FAINT, dt_tr)
        d.text((cxp, cells_top + dt_h + 5 * S), str(v), font=f_dd, fill=INK, anchor="la")
        wcell = max(_tw(d, k, f_dt, dt_tr), _tw(d, str(v), f_dd, 0))
        cxp += wcell + 44 * S

    item = spec["item"]
    item_px = 46
    f_item = F.get("inter", item_px)
    it_tr = -0.018 * item_px * S
    lines = _wrap(d, item, f_item, it_tr, left_w)
    if len(lines) > 2:
        item_px = 40
        f_item = F.get("inter", item_px)
        it_tr = -0.018 * item_px * S
        lines = _wrap(d, item, f_item, it_tr, left_w)[:2]
    ia, idsc = f_item.getmetrics()
    item_line = item_px * 1.1 * S
    item_h = item_line * (len(lines) - 1) + (ia + idsc)
    item_bottom = line_y - 20 * S
    iy = item_bottom - item_h
    for ln in lines:
        _draw_tracked(d, (left_l, iy), ln, f_item, TITLE, it_tr)
        iy += item_line

    f_k = F.get("mono600", 15)
    ka, kd = f_k.getmetrics()
    _draw_tracked(d, (left_l, (item_bottom - item_h) - 14 * S - (ka + kd)),
                  spec["review_kind"].upper(), f_k, ACCENT_INK, 0.2 * 15 * S)


# ============================================================ pelican glue ====
def _truthy(v):
    if isinstance(v, bool):
        return v
    return str(v).strip().lower() in ("true", "yes", "1", "on")


def _clean(text):
    """Title/item text -> plain string (strip any inline HTML + unescape)."""
    return unescape(re.sub(r"<[^>]+>", "", str(text or ""))).strip()


def _domain(siteurl):
    host = re.sub(r"^https?://", "", siteurl or "").strip("/").split("/")[0]
    return host or "andrewwegner.com"


def _build_spec(article, base, providers):
    meta = article.metadata
    category = str(getattr(article, "category", "") or "")
    spec = dict(base)
    is_review = str(meta.get("template", "")).lower() == "review" or ("score" in meta)
    if is_review:
        provider_key = str(meta.get("provider") or "Udemy")
        pinfo = providers.get(provider_key, {}) or {}
        item_type = pinfo.get("itemType", "Course")
        try:
            score = float(meta.get("score"))
        except (TypeError, ValueError):
            score = 0.0
        spec.update(
            kind="review",
            eyebrow=(category or "Review"),
            review_kind=str(meta.get("review_kind") or ("%s review" % item_type)),
            item=_clean(meta.get("revieweditem") or article.title),
            provider=pinfo.get("name", provider_key),
            workload=meta.get("workload"),
            score=score,
        )
    else:
        spec.update(kind="post", eyebrow=(category or "Article"), title=_clean(article.title))
    return spec


_HASH_KEYS = ("kind", "eyebrow", "title", "review_kind", "item", "provider",
              "workload", "score", "name", "role", "domain")


def _hash_spec(spec, version):
    payload = {k: spec.get(k) for k in _HASH_KEYS}
    payload["_v"] = version
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def generate_cards(article_generator, **kwargs):
    if Image is None:
        logger.warning("card_images: Pillow is not installed; no cards generated.")
        return
    settings = article_generator.settings
    if not settings.get("CARD_GENERATE", True):
        return

    siteurl = settings.get("SITEURL", "")
    out_root = os.path.abspath(settings.get("OUTPUT_PATH", "output"))
    rel_dir = str(settings.get("CARD_OUTPUT_DIR", "theme/img/cards")).strip("/")
    out_dir = os.path.join(out_root, *rel_dir.split("/"))
    os.makedirs(out_dir, exist_ok=True)

    theme = settings.get("THEME", "")
    base = dict(
        name=str(settings.get("CARD_NAME") or settings.get("AUTHOR_DISPLAY")
                 or settings.get("AUTHOR") or "Andrew Wegner"),
        role=str(settings.get("CARD_ROLE", "Engineering Leadership")),
        domain=str(settings.get("CARD_DOMAIN") or _domain(siteurl)),
        logo_path=(settings.get("CARD_LOGO") or os.path.join(theme, "static", "img", "logo-512.png")),
        headshot_path=(settings.get("CARD_HEADSHOT")
                       or os.path.join(theme, "static", "img", "wegner_headshot.png")),
        fonts_dir=(settings.get("CARD_FONT_DIR") or os.path.join(os.path.dirname(__file__), "fonts")),
    )
    providers = settings.get("REVIEW_PROVIDERS", {}) or {}
    version = str(settings.get("CARD_VERSION", "1"))
    try:
        supersample = max(1, int(settings.get("CARD_SUPERSAMPLE", SS)))
    except (TypeError, ValueError):
        supersample = SS
    # Supersample changes the pixels, so fold it into the cache key -> changing
    # it auto-invalidates cached cards without a manual CARD_VERSION bump.
    version = "%s-s%d" % (version, supersample)

    cache_dir = settings.get("CARD_CACHE_DIR")
    cache_manifest = {}
    if cache_dir and os.path.isdir(cache_dir):
        mp = os.path.join(cache_dir, MANIFEST_NAME)
        if os.path.isfile(mp):
            try:
                with open(mp, encoding="utf-8") as fh:
                    cache_manifest = json.load(fh)
            except Exception as exc:  # pragma: no cover
                logger.warning("card_images: could not read cache manifest: %s", exc)

    new_manifest = {}
    n_render = n_copy = 0
    for article in getattr(article_generator, "articles", []):
        meta = article.metadata
        if _truthy(meta.get("no_card")) or meta.get("cover"):
            continue
        slug = article.slug
        spec = _build_spec(article, base, providers)
        digest = _hash_spec(spec, version)
        out_path = os.path.join(out_dir, slug + ".png")
        cached = os.path.join(cache_dir, slug + ".png") if cache_dir else None

        reused = False
        if cache_manifest.get(slug) == digest and cached and os.path.isfile(cached):
            try:
                shutil.copyfile(cached, out_path)
                n_copy += 1
                reused = True
            except Exception as exc:  # pragma: no cover - fall through to render
                logger.warning("card_images: cache copy failed for %s (%s); rendering.", slug, exc)
        if not reused:
            try:
                render_card(spec, S=supersample).save(out_path, "PNG", optimize=True)
                n_render += 1
            except Exception as exc:
                logger.warning("card_images: render failed for %s: %s", slug, exc)
                continue
        article.card_image = "%s/%s.png" % (rel_dir, slug)
        new_manifest[slug] = digest

    try:
        with open(os.path.join(out_dir, MANIFEST_NAME), "w", encoding="utf-8") as fh:
            json.dump(new_manifest, fh, sort_keys=True, indent=0)
    except Exception as exc:  # pragma: no cover
        logger.warning("card_images: manifest write failed: %s", exc)

    logger.info("card_images: %d card(s) -- %d rendered, %d reused from cache.",
                len(new_manifest), n_render, n_copy)


def register():
    signals.article_generator_finalized.connect(generate_cards)
