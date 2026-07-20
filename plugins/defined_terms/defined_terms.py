# -*- coding: utf-8 -*-
"""
Defined Terms
=============

Pelican plugin that turns the ``definition`` admonition into a first-class,
linkable glossary entry -- as many per article as you like.

Authoring (ordinary Markdown, wherever the definition should appear in the
essay)::

    !!! definition "Management debt"
        The gap between how leadership is supposed to operate and how it
        actually operates.

That renders (via the standard ``admonition`` extension) as::

    <div class="admonition definition">
      <p class="admonition-title">Management debt</p>
      <p>The gap between how leadership...</p>
    </div>

This plugin then, per article:

1. Gives each definition block an anchor id (``term-<slug>``) so it can be
   linked and cited.
2. Rewrites inline ``<dfn>`` mentions of a defined term into a link down to that
   block, with the definition as a ``title`` tooltip::

       ...classic <dfn>management debt</dfn>...
       ->
       <a class="dfn-ref" href="#term-management-debt">
         <dfn title="The gap between...">management debt</dfn></a>

   A ``<dfn>`` whose text has no matching definition is left alone (it still
   gets the base ``<dfn>`` styling, just no link).
3. Exposes ``content.defined_terms`` -- a list of
   ``{"term", "definition", "slug"}`` dicts -- for
   ``partial/jsonld/definedterm.html`` to emit one ``DefinedTerm`` per term.

The visible block, the inline links, and the structured data all derive from the
same Markdown. Nothing is authored twice.
"""

import re
from bs4 import BeautifulSoup
from pelican import signals, contents
import logging

logger = logging.getLogger(__name__)

_SLUG_STRIP = re.compile(r"[^a-z0-9]+")


def _norm(text):
    return " ".join((text or "").split()).strip()


def _slug(text):
    return _SLUG_STRIP.sub("-", _norm(text).lower()).strip("-")


def define_terms(content):
    if isinstance(content, contents.Static):
        return
    if not getattr(content, "_content", None):
        return

    soup = BeautifulSoup(content._content, "html.parser")

    blocks = soup.select("div.admonition.definition")
    if not blocks:
        return

    terms = []
    by_key = {}  # normalized term -> (slug, definition)

    for block in blocks:
        title = block.find("p", class_="admonition-title")
        term = _norm(title.get_text()) if title else ""
        if not term:
            continue

        # Definition text = everything in the block except the title.
        parts = [
            child.get_text(" ", strip=True)
            for child in block.find_all(["p", "ul", "ol", "blockquote"])
            if child is not title
        ]
        definition = _norm(" ".join(parts))

        slug = "term-" + _slug(term)
        # Keep an author-supplied id if one is already present.
        if not block.get("id"):
            block["id"] = slug
        else:
            slug = block["id"]

        entry = {"term": term, "definition": definition, "slug": slug}
        terms.append(entry)
        by_key.setdefault(term.lower(), (slug, definition))

    # Link inline <dfn> mentions to their definition block.
    for dfn in soup.find_all("dfn"):
        key = _norm(dfn.get_text()).lower()
        match = by_key.get(key)
        if not match:
            continue
        slug, definition = match
        if definition and not dfn.get("title"):
            dfn["title"] = definition
        # Don't double-wrap if the author already put the dfn inside a link.
        if dfn.find_parent("a") is not None:
            continue
        link = soup.new_tag("a", href="#" + slug)
        link["class"] = "dfn-ref"
        dfn.insert_before(link)
        link.append(dfn.extract())

    content._content = soup.decode()

    if terms:
        content.defined_terms = terms
        logger.debug(
            "defined_terms: %d term(s) in %s", len(terms), content.source_path
        )


def register():
    signals.content_object_init.connect(define_terms)
