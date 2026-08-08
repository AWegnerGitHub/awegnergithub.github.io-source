# The theme

A near-white cool ground, one warm rust accent, no rounding. Two families and a
strict token table do the work that a decorative layer usually does.

## Type

| Family | Where | Why |
| --- | --- | --- |
| **Archivo** | prose, headings, all UI | A grotesque with enough width and weight range to carry hierarchy on its own |
| **JetBrains Mono** | dates, tallies, scores, code | A second voice for machine-recorded facts — timestamps, counts, and the code they describe |

Both are self-hosted in `static/fonts/`. No render-blocking third-party
stylesheet, no visitor IP leaked to a font CDN, and a local build never touches
the internet.

`base.html` preloads **both** faces and only those two. Mono earns its hint by
measurement rather than by argument: it renders inside the first viewport on
nine of the eleven page types, and on all 148 articles the topmost instance is
the `.article__date`, 142px down. On the two exceptions — About and 404 — it
still sets the footer's legal line, so the fetch happens on every page of the
site either way and the hint moves it earlier rather than adding it.
`tools/browser/font-critical-path.mjs` is the measurement; re-run it before
changing this.

`archivo-latin-ext.woff2` is deliberately **not** preloaded. Its `unicode-range`
covers accented Latin this content almost never uses, so hinting it would fetch
32KB per page to discard.

### The stylesheet ships unminified from here, on purpose

`site.css` is ~76KB in a local build and the markup links it by that name. That
is not a missing optimisation: the deploy workflow minifies it *in place* after
Pelican runs, down to ~38KB —

```
lightningcss-cli --minify -o output/theme/css/site.css output/theme/css/site.css
html-minifier-terser --input-dir output --output-dir output --file-ext html …
```

— so the linked name has to stay `site.css` or that step would minify a file
nobody requests. **Do not add a second minifier to this theme.** To check the
workflow's own step instead, run `tools/build/minify-check.py output-redesign`,
then `tools/browser/assets.mjs`, which asserts the minified sheet computes
identically on every element of five pages in both schemes at both widths.

Three rules hold everywhere:

- **Nothing renders below 12px.** Not labels, not counts, not the footer.
- **Anything that wraps sets line-height ≥ 1.3.** Display headings (`h1`, `h2`)
  are the deliberate exception at 1.08–1.22; they are short and set large.
- **The measure is the constraint, not the column.** Body copy is 17.5px in a
  606px column, 18.5px in a 688px one above 1180px and 19px in a 716px one above
  1500px — about the same number of characters per line each time, drawn larger.
  A wider monitor buys bigger type, wider grids and, on an essay page, wider code
  and images; never a longer line. See the "Wide screens" comment in `site.css`.

There is no tracked-caps micro-label tier. It was the root of three separate
findings in `audit/baseline.md` and it does not exist here.

## Colour

Every colour is a token in `:root`. **No rule below `:root` writes a raw colour
value** — no `oklch()`, no hex, no `rgb()`. That is the contract: if a colour is
wrong, exactly one line changes it. It still holds at zero violations across the
stylesheet.

**There is exactly one colour authored outside it, and it is not in the
stylesheet at all:** `partial/icon.html` writes the two `<meta name="theme-color">
values, `#f5f6f7` and `#14171c`. They have to be literal because the browser
reads them out of the head before any CSS parses — a token cannot be
dereferenced there. Each is its scheme's `--paper`, resolved by the browser
rather than converted by hand, and a behaviour test asserts the tag still
equals the ground the page paints in both schemes, so the duplication is
checked rather than trusted.

**`pelicanconf.py` pins both values** as `THEME_COLOR_LIGHT` /
`THEME_COLOR_DARK`, which means a config value beats the template's default. So
moving `--paper` takes *three* edits, not one: `:root` here, and those two keys.
That is not hypothetical — the Cream→Chalk change hit it, and the browser chrome
kept painting the old ground until the config caught up. Run
`tools/browser/paper-hex.mjs` to get the pair, and `theme-color.mjs` fails until
they agree.

38 tokens in four groups: surfaces (`--paper`, `--paper-sunk`, `--card`,
`--zebra`, `--wash`, `--code-bg`), ink (`--ink` … `--ink-faint`, `--ink-cat`),
lines (`--rule*`, `--border`, `--*-border`), accent (`--accent`,
`--accent-hover`, `--on-accent`), plus five callout hues.

Every ink token clears **WCAG AA (4.5:1)** against every surface it renders on,
in both schemes. Lowest margins:

| | light | dark |
| --- | ---: | ---: |
| `--ink-faint` on `--wash` | 4.54 | 5.06 |
| `--ink-faint` on `--zebra-hover` | 4.61 | 4.52 |
| `--accent` on `--wash` | 4.85 | 5.96 |
| `--accent` on `--paper-sunk` | 5.05 | 6.75 |
| `--accent` on `--paper` | 5.44 | 7.50 |
| `--on-accent` on `--accent` | 5.71 | 7.85 |

The accent carries text in three places, not just links: the header's role line
(`.brand__role`), the *first item only* of the identity block's role line
(`.hero__role-lead` — the rest of that line is `--ink-muted`), and the year label
in the home archive index (`.mini-year__label`). Those are the rows to check
first if the accent ever moves.

**The shipped ground is Chalk**, chosen 2026-07-29 from the twelve candidates in
`palettes/PALETTES.md`. Its ramp is that file's Chalk table verbatim, so a
change belongs there first and here second. Chalk moves hue and chroma only —
every lightness value is the one the design was drawn with, which is why the
contrast table above barely moved when the ground changed.

The cool cast lives in the panels, not in the sheet: `--paper-sunk`, `--zebra`,
`--wash`, `--code-bg` and `--row-hover` all carry their full tint, and that is
where a reader actually sees it — the band behind a title, the alternating
archive rows, the tint behind a pull quote. `--paper` itself is
`oklch(0.972 0.002 255)` → `rgb(245, 246, 247)`, which reads as white.

Two things follow from a cool ground, and both are simplifications. The
detector's `cream-palette` rule **cannot fire on it at all** — that rule needs a
warm ordering, red ≥ green ≥ blue, and this is the opposite. The old ground was
capped at `0.005` chroma purely to stay one 8-bit step under that rule; on a
cool ground the cap does not need to exist, so every surface carries its full
tint. And the accent stays warm, which is the whole reason Chalk was picked over
the other four in its wave: one warm mark on a cool page.

**Which scheme is live** is decided in three steps: light by default, dark if the
operating system asks for it, and whatever the reader picked with the header
toggle over both. Light leads because this is a light design that also has a dark
mode; the OS still gets a vote because a reader who set their machine to dark has
already answered the question, and ignoring that is overriding a preference
rather than setting a default. The choice rides on `<html data-theme>`, written
before first paint by an inline script in `base.html` and persisted by `site.js`.

There is no fourth step to add, and it is worth knowing why: nothing exposes "the
reader never chose". `prefers-color-scheme: no-preference` was dropped from the
spec and never matches — Chrome reports `dark` even when asked to emulate it —
and an OS set to auto reports plain `dark` once it is dark out. So step one means
"the browser says light", which is what every browser says absent a dark
preference.

Because the dark ramp has to be reachable from a media query *and* from an
attribute selector, and CSS cannot share one declaration block between the two,
it is written twice — the only repeated values in the file. Keep them in sync;
`audit/2026-07-27_thoughts_pass.md` shows how to check it in a dozen lines.
Nothing else in the stylesheet knows which scheme is live.

### One rule to know before putting a link on the accent

```css
a:hover { color: var(--accent); }
```

That is `(0,1,1)`. A class-only `color` is `(0,1,0)`, so on any link that already
sits **on** the accent this rule wins and paints the label in the exact colour of
the ground beneath it — **1:1 contrast, an invisible word.** `.btn--accent:hover`
has always restated `color: var(--on-accent)` for that reason;
`.carousel__item:hover` and `.idea:hover` set `color: inherit` for the same one.

`.skip-link` and `.article__cat` did not, and shipped with the defect until
2026-07-30. It survived five audits because all five measured the page at rest,
and it is not a token-pair problem a colour table could have caught — it is a
specificity interaction. **Any new component that puts a link on `--accent` must
restate `--on-accent` in its own hover rule.**
`tools/browser/measure.mjs` forces the state and measures the pixels, so a
repeat fails a check rather than shipping.

## Width

**One shell, every page.** `--shell` is declared once, on `:root`, and the header,
the title band, the body and the footer all measure it — so moving from the home
page to an essay does not move the page edges. It used to be re-declared per page
type on `<body>`, which is inside `:root`, so an inherited body value beat the
root one and every change had to be made twice. Do not reintroduce that; if a
page type seems to need a different width, the question to ask first is why the
frame should move.

| | ≤1179px | ≥1180px | ≥1500px |
| --- | --- | --- | --- |
| shell | 980 | 1120 | `clamp(1280, 100vw − 280, 1640)` |
| gutter | 40 | 52 | 52 |
| text column | 606 @ 17.5px | 688 @ 18.5px | 696–1056 @ 20px |
| contents rail | 244 | 268 | 400 |

Past 1500px the shell tracks the window rather than stepping again, so a 2560px
monitor is not handed a page sized for a 1500px one; 1640 is where more width
stops buying anything.

**The text column has no max-width above 1500px.** It runs the full grid track,
so the only thing between the essay and the contents rail is the 80px gap. At
1920 that is a 1056px line — around 120 characters, well past the 60–80 that
typography convention and the detector's `line-length` rule both aim at.

That is deliberate and it was Andy's call, made against the alternative (a ~300px
band of dead space between the text and the rail, which is what a capped column
produces inside a uniform frame). Two things follow from it and should not be
quietly undone:

- **The leading is 1.75, not 1.68.** On a line this long the hard part is
  finding the start of the next one, and the extra leading is what pays for it.
- **It costs 63 `line-length` findings at 1920** (0 at 1280 and 390, which are
  the viewports the standing detector scan uses — so the headline audit number
  does not show this). If you want to trade back, the dial is the body font
  size: the column width is set by the frame, so a larger face means fewer
  characters on the same line.

One trap, walked into twice: **stepping the rail wider at a breakpoint where the
shell steps by less makes the text column shrink as the window grows.** At ≥1500
the shell floor is 1280, so the rail is 400 because 1280 − 104 − 400 − 80 = 696,
which has to clear the 688 the tier below had. Check that arithmetic before
changing either number.

## Shape and motion

- **Border radius is 0.** The only `border-radius` declarations in the file are
  the three inside `@keyframes morph` and the one that cancels them under
  reduced motion.
- **No accent border wider than 2px, on any edge.** Emphasis rides a 2px *top*
  rule (`.pull`, `.prose blockquote`, `.prose .admonition`), never a thick left
  tab. A callout also carries a 1px frame on the other three edges — see
  "Callouts" below for why, and note that 1px surround plus 2px top is still
  inside the rule. Containment is not a tab.
- **No gradients and no background images.** Every text node sits on a solid,
  measurable ground.
- **Reduced motion is targeted, not global.** The decorative morph loop stops
  and hover transforms are cancelled; the 140–220ms colour and border
  transitions that report state stay, because they are feedback.
- **The light/dark change cross-fades**, at `--theme-fade` (180ms, `ease` — in
  the vocabulary). It is the one rule in the file that reaches every element,
  and it exists for the length of the change only: `site.js` puts
  `.theme-fade` on `<html>`, the stylesheet's last block does the rest, and the
  class comes off 50ms after the duration. **`--theme-fade: 0ms` turns it off**
  and is what `prefers-reduced-motion` resolves it to. It costs a long frame at
  the press — measured at +30ms on an article and +70ms on `/archives.html`,
  which is 1010 elements — and the block at the end of `site.css` carries the
  full numbers and the alternative that would avoid them.

## JavaScript

`static/js/site.js` is enhancement only. With it disabled: every card renders,
every archive row is present, the contents list is a plain anchor list, the
paginated index still pages, the page still follows the system's light/dark
setting, and no control appears that cannot act — the
carousel steppers, the category chips, the sort toggles and the "Older posts"
button all ship `hidden` and are revealed by their own module; the theme toggle
is revealed by the `has-js` class the inline script writes.

Every scroll handler is batched through `requestAnimationFrame`, so a scroll
event never does a layout read followed by a style write.

Modules: theme toggle, reading progress, identity→header brand handoff,
carousel, category filters, load older posts, contents rail, taxonomy sort,
wide-table scroll wrapper.

**The wide-table module has no live surface.** It wraps `.prose table` in a
focusable scroll region and writes `data-more` naming the edges that still have
content behind them, which the stylesheet paints as an inset shadow — the only
cue a reader gets that a table is cut off. But this site has no tables at all:
the `tables` Markdown extension is not enabled, no post contains a pipe table or
a raw `<table>`, and no template emits one. The module runs over an empty
NodeList on all 233 pages. It is tested against a table injected into the served
HTML (`tools/browser/tables.mjs`), so the mechanism is verified even though the
site never exercises it. Two things follow: enabling tables is a one-word change
to a frozen config file and therefore Andy's call, and with scripting off there
is no wrapper, so a wide table would overflow the document — that suite measures
it (346px at 390w) rather than asserting it away.

Reading progress renders only on articles and reviews — `article.html` sets
`track_scroll`, `partial/nav.html` renders the bar from it. On a landing page or
an index there is no "how far through" to report. The carousel stepper carries no
position readout for the same reason: rotation never changes how many cards are
on screen, so "3 of 7" was true before the first click and after every one.

There is one other script: eight lines inline in `base.html`, which have to run
before the first paint or a reader who chose dark would see a flash of light
first. They do the least possible — add `has-js`, and copy a stored choice onto
`<html data-theme>`. No choice stored means no attribute written, which is what
keeps a visitor who never touched the toggle following their system setting,
live, as it changes. `site.js` owns the rest: the button's wiring,
its accessible name, and keeping `<meta name="theme-color">` on the same ground
as the page. It never sets a colour — it sets the attribute the stylesheet keys
off, and reads `--paper` back out of the token table for the meta tag.

The brand handoff hides the header brand with `visibility` rather than
`opacity` alone, so it is never an invisible tab stop, and focus held on it pins
it visible. It runs on any page whose template sets `brand_handoff` — the home
hero and About, both of which open with the identity block.

**Load older posts** is the one module that fetches. It reads the next index
page from `<link rel="next">`, lifts its `.mini-year` groups out and appends
them to the panel already on screen: years merge rather than repeat, the tally
follows, and a category first seen further down the archive gains a filter chip.
Two consequences to keep in mind when touching it — the filter module re-reads
its rows on a `filters:refresh` event rather than closing over one snapshot of
them, and disabling the focused button hands focus to `<body>`, so the module
puts it back (on the button, or on the archive link once the control is gone).

## Callouts

A callout is derived entirely from one hue: `--adm`. The tint, the frame and
the title colour all come from it, so a new type is still one line.

Two things about that derivation are worth reading before changing it, because
both were defects and both were invisible on the shipped cream ramp.

**`color-mix` runs `in oklab`, not `in oklch`, and that is not a preference.**
`oklch` interpolates hue along an arc: an amber at hue 72 mixed into a ground at
hue 255 travels through violet, so the tint pushes the ground *away* from the
hue it is supposed to be tinting it with. Measured as a unit vector against the
amber's own direction, where a negative number means it moved the wrong way:

| | old, 8% | old, 30% | now |
| --- | ---: | ---: | ---: |
| cream | +0.98 | +0.98 | +1.00 |
| Chalk | **−0.84** | **−0.24** | +0.99 |
| Blueprint | **−0.67** | **−0.20** | +1.00 |

Raising the percentage never fixes it. Cream passes either way, because `--warn`
is hue 72 and `--paper-sunk` is hue 80 and there is no arc to travel — which is
why this survived until a cool palette existed. `tools/browser/callouts.mjs`
asserts the direction, so it cannot come back.

**The ground is `--card`, not `--paper-sunk`.** Code sits on `--paper-sunk`'s
neighbour `--code-bg`, so a callout that started from the same step was
competing with every code block on the page at the same lightness, the same
width and the same 2px top rule. Starting from `--card` and adding a 1px frame
makes a callout a *raised, bounded* object and leaves code a recessed band. The
frame is also what carries a callout with no title.

`--adm-tint` is 18% in light and **22% in dark**, and the dark ceiling is
contrast, not taste: the title is painted in `--adm` on this ground, `--danger`
is the darkest dark callout hue at `oklch(0.78 …)`, and every extra point of
tint lightens the ground under it. Across twelve palettes, 22% leaves the danger
title at 4.89:1 and 26% drops it to 4.45 — under AA.

## Temporary: the palette switcher

`thoughts.md` #26. A dev control in the left gutter of every page that repaints
the site in any of the twelve ground candidates in `palettes/PALETTES.md`, so a
palette can be judged on a 148-row archive and a code-heavy essay rather than on
a swatch card. **It is scaffolding and it is meant to be deleted**, so it was
built to come out cleanly:

- **Nothing in `site.css` or `site.js` was changed to make it work.** It reads
  one attribute they do not (`data-palette`) and writes the `theme-color` tags,
  which it hands back exactly as `site.js` left them whenever no palette is
  chosen — the failure mode that costs nothing to have and is invisible without
  a test, so there is one.
- **Six things to delete**, listed in `partial/palette_switcher.html`: two
  include lines in `base.html`, three partials, two stylesheets, one script.
- **`PALETTE_SWITCHER = False`** in a settings file removes every trace from the
  rendered HTML without deleting anything. Verified by probe build: 0 of 233
  pages mention it, and the only diff against a switcher build is the switcher.

The colour data is generated. `palettes/make-switcher-css.py` reads
`PALETTES.md` and writes `static/css/palette-tokens.css` (12 palettes × 32
tokens × 2 schemes) and `partial/palette_switcher_options.html`; both say so at
the top. `static/css/palette-switch.css` is the control's own styling and is
hand-written — which is why they are two files. The option list is grouped into
the two waves, and that grouping is generated too: the wave sentinels live in
`PALETTES.md`, so adding a third wave needs no edit here.

One thing to know before touching the generated stylesheet: its selectors carry
the *same scheme condition `site.css` uses*, plus the palette attribute. A
single `:root[data-palette=x]` block would tie with `:root[data-theme="dark"]`
on specificity and win on source order, dragging a dark page back to a light
ramp. The generator's header comment carries the arithmetic.

This is also the one thing in the theme that reads a colour out of a file other
than `site.css`, which is why the Colour section above says "exactly one colour
authored outside `:root`" and means it: the palette ramps are still tokens in
`:root`, just written by a script.

## Structured data

`templates/partial/jsonld/` is copied byte-for-byte from the current theme and
must stay that way. The redesign is a UI change; the site's structured data is
not part of it.
