"""Strip configured URLs from the generated sitemap.xml.

The bundled `extended_sitemap` plugin walks every DIRECT_TEMPLATES entry and
emits a sitemap node with no exclusion option. `404.html` is in
DIRECT_TEMPLATES so Pelican writes `output/404.html` for GitHub Pages' custom
404 support — but the page is `noindex` and shouldn't be in the sitemap.

Set `SITEMAP_EXCLUDE` in pelicanconf to a list of paths (e.g. ["/404.html"]).
Each path is matched against the full `<loc>` URL after prepending SITEURL.
"""
import re
from pathlib import Path

from pelican import signals


_URL_BLOCK = re.compile(r"<url>\s*<loc>(?P<loc>[^<]+)</loc>.*?</url>\s*", re.DOTALL)


def filter_sitemap(pelican_obj):
    excludes = pelican_obj.settings.get("SITEMAP_EXCLUDE") or []
    if not excludes:
        return
    sitemap = Path(pelican_obj.output_path) / "sitemap.xml"
    if not sitemap.exists():
        return
    site_url = (pelican_obj.settings.get("SITEURL") or "").rstrip("/")
    full = {site_url + p if p.startswith("/") else p for p in excludes}
    text = sitemap.read_text(encoding="utf-8")
    new_text = _URL_BLOCK.sub(
        lambda m: "" if m.group("loc").strip() in full else m.group(0),
        text,
    )
    if new_text != text:
        sitemap.write_text(new_text, encoding="utf-8")


def register():
    signals.finalized.connect(filter_sitemap)
