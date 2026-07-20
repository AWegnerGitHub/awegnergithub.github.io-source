# -*- coding: utf-8 -*-
"""
Extract FAQ
===========

Pelican plugin that lifts a "Common questions" Q&A section out of an article's
rendered content and exposes it as structured data for the templates.

Two outputs, one source (the Markdown the author already wrote):

* ``content.faq`` -- a list of dicts, one per question::

      {"question": str,   # visible question text (headerlink stripped)
       "answer":   str,   # answer HTML (paragraphs, lists, links, ...)
       "text":     str,   # answer as plain text, for JSON-LD
       "slug":     str}   # anchor id, reused from the source <h3> id

  ``partial/faq_section.html`` renders this as the same ``<dl class="faq">``
  markup the About page uses (visual parity), and
  ``partial/jsonld/faq_article.html`` emits the matching ``FAQPage`` JSON-LD.

* The section is *removed* from ``content._content`` so the questions are not
  rendered twice -- once as raw Markdown, once as the styled block. This mirrors
  how ``extract_toc`` pulls the ToC out of the body.

``content.faq_heading`` / ``content.faq_id`` carry the section's visible heading
text and its anchor id (e.g. ``common-questions``) so the ToC link keeps
resolving after the move.

Authoring format (ordinary Markdown, at the bottom of the essay)::

    ## Common questions

    ### What is management debt?

    Management debt is the gap between how leadership is supposed to operate
    and how it actually operates.

    ### How is it different from technical debt?

    Technical debt lives in the codebase...

The heading is configurable via ``FAQ_HEADING`` (default "Common questions");
matching is case-insensitive. Everything between that ``<h2>`` and the next
``<h2>``/``<h1>`` is FAQ content; each ``<h3>`` is a question and the block
elements beneath it are its answer.
"""

from bs4 import BeautifulSoup
from pelican import signals, contents
import logging

logger = logging.getLogger(__name__)

DEFAULT_HEADING = "Common questions"


def _norm(text):
    """Collapse whitespace to a single space and strip."""
    return " ".join((text or "").split()).strip()


def _strip_headerlink(tag):
    """Remove the toc extension's permalink anchor (¶) from a heading, in place."""
    for a in tag.find_all("a", class_="headerlink"):
        a.decompose()


def _clean_text(tag):
    """Heading text with the toc permalink anchor removed, without mutating the
    original tag (used to match the FAQ heading -- `permalink=true` appends a ¶
    that would otherwise defeat a plain get_text() comparison)."""
    clone = BeautifulSoup(str(tag), "html.parser")
    for a in clone.find_all("a", class_="headerlink"):
        a.decompose()
    return _norm(clone.get_text())


def extract_faq(content):
    # Only articles/pages have a Q&A body; skip static assets.
    if isinstance(content, contents.Static):
        return
    if not getattr(content, "_content", None):
        return

    heading = content.settings.get("FAQ_HEADING", DEFAULT_HEADING)
    target = _norm(heading).lower()

    soup = BeautifulSoup(content._content, "html.parser")

    faq_h2 = next(
        (h for h in soup.find_all("h2") if _clean_text(h).lower() == target),
        None,
    )
    if faq_h2 is None:
        return

    items = []
    current = None          # dict for the question being built
    answer_nodes = []       # raw sibling tags making up the current answer
    section_nodes = []      # every node to remove from the body afterwards

    def flush():
        if current is None:
            return
        answer_html = "".join(str(n) for n in answer_nodes).strip()
        answer_text = _norm(
            " ".join(n.get_text(" ", strip=True) for n in answer_nodes)
        )
        if answer_html and answer_text:
            current["answer"] = answer_html
            current["text"] = answer_text
            items.append(current)

    for sib in faq_h2.find_next_siblings():
        if sib.name in ("h1", "h2"):
            break  # end of the FAQ section
        section_nodes.append(sib)
        if sib.name == "h3":
            flush()
            _strip_headerlink(sib)
            question = _norm(sib.get_text())
            slug = sib.get("id") or _norm(question).lower().replace(" ", "-")
            current = {"question": question, "answer": "", "text": "", "slug": slug}
            answer_nodes = []
        elif current is not None:
            answer_nodes.append(sib)
    flush()

    if not items:
        return

    # Record the heading text + anchor before we drop it, so the ToC link still
    # resolves against the styled block the template renders.
    _strip_headerlink(faq_h2)
    content.faq = items
    content.faq_heading = _norm(faq_h2.get_text()) or heading
    content.faq_id = faq_h2.get("id") or target.replace(" ", "-")

    # Remove the whole section from the visible body (it is re-rendered, styled,
    # by partial/faq_section.html).
    for node in section_nodes:
        node.extract()
    faq_h2.extract()
    content._content = soup.decode()

    logger.debug(
        "extract_faq: %d Q&A pair(s) in %s", len(items), content.source_path
    )


def register():
    signals.content_object_init.connect(extract_faq)
