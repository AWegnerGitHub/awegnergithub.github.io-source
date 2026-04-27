# Pelican theme — Andrew Wegner redesign

Drop-in Pelican theme that renders the redesign. Rename the directory to whatever you want and point `THEME` at it in `pelicanconf.py` — nothing inside references the directory name.

## Install

```python
# pelicanconf.py
THEME = 'path/to/this/directory'
```

## Expected / consumed config variables

### Required (Pelican built-ins)
- `SITENAME`, `SITEURL`, `AUTHOR`, `DEFAULT_LANG`

### Recommended
- `SITESUBTITLE` — shown in `<title>` when present
- `SITEDESCRIPTION` — meta description + Blog JSON-LD
- `SITELOGO` — path to the logo image relative to site root (used in Blog JSON-LD + OG image fallback)
- `FAVICON`, `FAVICON_32X32`, `FAVICON_16X16`, `APPLETOUCHICON`, `SITEMANIFEST`, `BROWSER_COLOR`
- `FEED_ALL_ATOM` / `FEED_ALL_RSS` / `CATEGORY_FEED_ATOM` / `TAG_FEED_ATOM` — standard Pelican feed config
- `MENUITEMS` — list of `(title, url)` tuples for the main nav. If absent the theme falls back to a built-in nav (Archives / Categories / Tags / About).
- `CONTACT_EMAIL` — powers the top-right "Contact Me" button + footer mailto
- `RESUME_URL`, `RESUME_LABEL` — "Download résumé (PDF)" button
- `SOCIAL_META` — list of `(label, url, display_text)` tuples for the footer meta block (LinkedIn / GitHub / Stack Overflow / etc.)
- `COPYRIGHT_YEAR`

### Redesign-specific (new with this theme)

```python
# Headshot
HEADSHOT = 'wegner_headshot.png'      # filename in theme static/img/
HEADSHOT_MORPH = True                  # default True: morphing blob animation. Set False for static circle.

# Author display strings
AUTHOR_GIVEN = 'Andrew'
AUTHOR_FAMILY = 'Wegner'
AUTHOR_ROLE = 'VP, Strategic Software'
AUTHOR_ROLE_LINES = ['VP,', 'Strategic Software']   # how the nav wordmark and sidebar stack the role on two lines

# Home page content (all optional — sections render only if present)
LANDING_HERO = {
    'kicker':   'Engineering leader · Writer · Moderator',
    'headline': 'Building the teams that <em>build the systems</em>.',   # HTML allowed
    'sub':      'I lead, grow and mentor engineering organizations ...',
    'primary_cta':   {'url': '#writing', 'label': 'Read the latest essay'},
    'secondary_cta': {'url': '/archives.html', 'label': 'Browse all writing'},
    'meta': [
        ('Currently',    'VP, Strategic Software'),
        ('Previously',   'VP Eng · Director Eng'),
        ('Writing since', '2019'),
    ],
}
LANDING_METRICS = [
    ('40+', 'Engineers in largest org led'),
    ('5',   'Industries: telecom, logistics, hiring, manufacturing'),
    ('15+', 'Years shipping software end-to-end'),
    ('3',   'VP / Director engineering roles'),
]
LANDING_PRINCIPLES_HEAD = (
    'Four ideas that shape how I run engineering orgs.',
    'Drawn from fifteen years building teams across telecom, logistics, hiring and manufacturing.',
)
LANDING_PRINCIPLES = [
    # 3-tuple: non-clickable card.
    ('01', "Distance doesn't diminish performance.", '...'),
    # 4-tuple: whole card becomes a link to the given URL. Internal paths
    # starting with "/" get SITEURL prepended; full https:// URLs are used
    # as-is.
    ('02', 'Hire for what actually predicts the job.', '...', '/some-article-slug.html'),
    ('03', 'Technical debt is a leadership problem.', '...'),
    ('04', 'Grow engineers as the product.', '...'),
]

# Footer copy (all optional; sensible defaults)
FOOTER_KICKER   = 'GET IN TOUCH'
FOOTER_HEADLINE = 'Currently open to VP Engineering and CTO conversations.'
FOOTER_SUB      = "I'm selective about what I take on, but always happy to talk about engineering leadership, distributed teams, and hiring."
```

### Review posts
Set `template: review` in markdown front-matter plus:
- `revieweditem`, `score`, `price`, `saleprice`, `workload`, `provider`

`provider` keys into `REVIEW_PROVIDERS` (from the old theme; keep as-is). The theme handles Course-type and Product-type reviews; add the `itemType` key in each provider entry.

### FAQ page (About)
Set `FAQ_QUESTIONS = [('Question text?', 'Answer HTML'), ...]`. Only renders inside the page whose slug is `about`. Emits FAQPage JSON-LD automatically.

### Analytics
- `HEAP_ANALYTICS` — project ID. Autocapture only (no identify / track calls are emitted by the theme).

### Plugins (must be enabled in `pelicanconf.py`)
The theme reads these plugin-injected values:
- `extract_toc` → `article.toc`
- `series`      → `article.series.index`, `article.series.all_previous`, `article.series.all_next`
- `neighbors`   → `article.prev_article`, `article.next_article`
- `post_stats`  → `article.stats.read_mins`
- `keyboard`    → no template-side integration (just enables `[kbd]` markdown)

All five are expected to already be in `PLUGINS`.

## What's in the theme

```
templates/
├── base.html              everything else extends this
├── index.html             home (hero + metrics + principles + feed)
├── article.html           standard post
├── review.html            review post (adds review card + Review JSON-LD)
├── page.html              flat page (About uses FAQ_QUESTIONS)
├── category.html          single category listing
├── tag.html               single tag listing
├── categories.html        categories index with count bars + stats
├── tags.html              tags index with count bars + stats
├── archives.html          year-grouped title-only list
└── partial/
    ├── nav.html, sidebar.html, footer.html
    ├── breadcrumb.html, pagination.html, post_nav.html, series_block.html
    ├── post_card.html, archive_row.html, review_card.html
    ├── toc.html, author_bio.html
    ├── heap.html, og.html, og_article.html, feed.html, icon.html
    └── jsonld/
        ├── blog.html              Blog (every page)
        ├── blogposting.html       BlogPosting (articles + reviews)
        ├── review.html            Review / Course / Product (reviews)
        ├── breadcrumb.html        BreadcrumbList (emitted by breadcrumb.html)
        ├── faq.html               FAQPage (About)
        └── person.html            ProfilePage / Person — verbatim port from old theme
static/
├── css/site.css           single stylesheet; light theme only
└── img/wegner_headshot.png
```

## Notes

- **Zero path references to this directory's name.** Every asset URL uses `{{ SITEURL }}/{{ THEME_STATIC_DIR|default('theme') }}/...`. You can rename `pelican-template/` to anything.
- **Sidebar ↔ nav-wordmark scroll animation** is a small inline `<script>` at the end of `base.html` — no build step, no framework.
- **Light theme only.** The `.dark` CSS was stripped during the port. If you want dark mode back, reintroduce the `.site.dark { ... }` blocks from the prototype's `styles/site.css`.
- **The morphing blob animation** around the headshot is on by default. Set `HEADSHOT_MORPH = False` to get a plain circle.
