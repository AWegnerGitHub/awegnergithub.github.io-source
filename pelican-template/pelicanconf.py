# pelicanconf.py - copied from the upstream -source repo and edited for the
# redesign theme. Drop this into the -source repo's root (overwriting the
# existing pelicanconf.py) and point THEME at this theme directory.
#
# Changes from upstream are grouped below under "REDESIGN - NEW CONFIG".
# Nothing else in this file was removed - all upstream config is preserved so
# plugins, feeds, static paths, AUTHORS, REVIEW_PROVIDERS, FAQ_QUESTIONS, etc.
# continue to work unchanged.

import datetime

AUTHOR = "Andy Wegner"
SITENAME = "Andrew Wegner | Ponderings of an Andy"
SITEURL = "https://andrewwegner.com"
# SITEURL = ""
SITESUBTITLE = "Can that be automated?"
# SITEDESCRIPTION = "Articles and reviews covering thoughts on work place leadership, technical course reviews, and other ponderings of Andy Wegner"
SITEDESCRIPTION = "Andrew Wegner (Andy Wegner) - VP Strategic Software at Zayo, Stack Overflow moderator. Engineering leadership insights, Python tutorials, and technical articles from nearly 20 years of building global software teams."
COPYRIGHT_YEAR = datetime.date.today().year
COPYRIGHT_NAME = "Andrew Wegner"
SITELOGO = "/theme/img/wegner_headshot.png"


PATH = "content/"
READERS = {"html": None}
THEME = "pelican-template/"
OUTPUT_PATH = "output/"

TIMEZONE = "America/Chicago"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
FEED_MAX_ITEMS = None

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["series", "extract_toc", "neighbors", "keyboard", "extended_sitemap"]

TOC = {"TOC_HEADERS": "^h[1-3]"}

MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "codehilight code"},
        "markdown.extensions.toc": {"permalink": "true"},
        "markdown.extensions.admonition": {},
        "customblocks": {},
    }
}

JINJA_ENVIRONMENT = {"extensions": ["jinja2.ext.do"]}


PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"

# Top-nav menu (rendered by partial/nav.html)
MENUITEMS = (
    ("About",      "/about/"),
    ("Archives",   "/archives.html"),
    ("Categories", "/categories.html"),
    ("Tags",       "/tags.html"),
)

STATIC_PATHS = [
    "images",
    "extra/CNAME",
    "extra/google8e079521c0d93c27.html",
    "extra/keybase.txt",
    "extra/BingSiteAuth.xml",
    "extra/favicon.ico",
    "extra/apple-touch-icon.png",
    "extra/favicon-32x32.png",
    "extra/favicon-16x16.png",
    "extra/site.webmanifest",
    "extra/robots.txt",
    "extra/resume.pdf",
    "pages/about.html",
]
EXTRA_PATH_METADATA = {
    r"extra/CNAME": {"path": "CNAME"},
    r"extra/google8e079521c0d93c27.html": {"path": "google8e079521c0d93c27.html"},
    r"extra/robots.txt": {"path": "robots.txt"},
    r"extra/keybase.txt": {"path": "keybase.txt"},
    r"extra/BingSiteAuth.xml": {"path": "BingSiteAuth.xml"},
    r"images/": {"path": "images/"},
    r"extra/favicon.ico": {"path": "favicon.ico"},
    r"extra/apple-touch-icon.png": {"path": "apple-touch-icon.png"},
    r"extra/favicon-32x32.png": {"path": "favicon-32x32.png"},
    r"extra/favicon-16x16.png": {"path": "favicon-16x16.png"},
    r"extra/site.webmanifest": {"path": "site.webmanifest"},
    r"extra/resume.pdf": {"path": "resume.pdf"},
    r"pages/about.html": {"path": "about.html"},
}

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True


AUTHORS = {
    "Andy Wegner": {
        "image": "wegner_headshot.png",
        "blurb": """ is a father, an engineer and a computer scientist. He is interested in online
            community building, tinkering with new code and building new applications.
            He writes about his experiences with each of these.""",
        "friendly_name": "Andy Wegner",
        "url": "https://andrewwegner.com/about/",
    }
}

REVIEW_PROVIDERS = {
    "Udemy": {
        "type": "Organization",
        "name": "Udemy",
        "sameAs": "https://www.udemy.com/",
        "itemType": "Course",
    },
    "Coursera": {
        "type": "Organization",
        "name": "Coursera",
        "sameAs": "https://www.coursera.org/",
        "itemType": "Course",
    },
    "LevelUp": {
        "type": "Organization",
        "name": "LevelUp",
        "sameAs": "https://levelup.gitlab.com/",
        "itemType": "Course",
    },
    "RealPython": {
        "type": "Organization",
        "name": "Real Python",
        "sameAs": "https://realpython.com/",
        "itemType": "Course",
    },
    "RiseGardens": {
        "type": "Organization",
        "name": "Rise Gardens",
        "sameAs": "https://risegardens.com/",
        "itemType": "Product",
    },
}

EXTENDED_SITEMAP_PLUGIN = {
    "priorities": {"index": 1.0, "articles": 0.8, "pages": 0.5, "others": 0.4},
    "changefrequencies": {
        "index": "daily",
        "articles": "weekly",
        "pages": "weekly",
        "others": "monthly",
    },
}

FAQ_QUESTIONS = [
    (
        "Who is Andrew (Andy) Wegner?",
        "Andy is an engineering leader with experience at companies ranging in size and industry. He's led teams at pre-seed startups and large corporations. He writes a blog on his experiences in leadership, technology, and his hobbies.",
    ),
    (
        "What is Andrew's current role?",
        "Andy is currently employed at Zayo Group as Vice President Product, Strategic Software.",
    ),
    (
        "What technology stack is Andrew most familiar with?",
        "Andy is most familiar with Python, with over 15 years of hands on experience in the language and ecosystem. He's familiar with a variety of relational databases, including Postgres, MySQL, Oracle and Teradata. ",
    ),
    (
        "What industries has Andrew worked in?",
        "Andy has worked in Telecommunications, Logistics, Manufacturing, Human Resources Information Systems, and AdTech.",
    ),
    (
        "Is Andrew Wegner a Stack Overflow Moderator?",
        "Yes. Andy was elected to as a Stack Overflow moderator in August 2017. He was appointed Moderator Pro Tempore on Hardware Recommendations in October 2015 (and stepped down in 2024), and Moderator Pro Tempore on Community Building in August 2014 (and stepped down in 2024).",
    ),
    (
        "Does Andrew Wegner have a GitHub Account?",
        "Yes. Andy maintains a GitHub account: AWegnerGithub",
    ),
    (
        "Does Andrew do consulting work?",
        "Yes. Andy does consulting work. Previously, consulting work was done in a development capacity utilizing Python. More recently, Andy provides leadership mentoring or fractional CTO services.",
    ),
    (
        "What leadership experience does Andrew have?",
        "Andy has held Vice President level roles in software engineering organizations at Zayo and PacketFabric. He was a fractional CTO at White Square Media, a video AdTech company. He's held Director of Engineering level roles at FleetOps aka Class8 and Woven Teams. These experiences include building, growing and mentoring global engineering teams. Prior to this, he was an individual contributor and team lead at Caterpillar.",
    ),
    (
        "What is Andew's educational background?",
        "Andy holds a Master of Engineering in Information Assurance degree from Iowa State University and a Bachelor of Science in Computer Science with a Minor in Psychology degree from Northern Illinois University.",
    ),
]


HEAP_ANALYTICS = 653100411
BROWSER_COLOR = "#080019"
FAVICON = "/favicon.ico"
APPLETOUCHICON = "/apple-touch-icon.png"
FAVICON32X32 = "/favicon-32x32.png"
FAVICON16X16 = "/favicon-16x16.png"
SITEMANIFEST = "/site.webmanifest"

# Disable Author Pages (it's just me)
AUTHORS_SAVE_AS = ""
AUTHORS_URL = ""
AUTHOR_SAVE_AS = ""
AUTHOR_URL = ""


# =============================================================================
# REDESIGN - NEW CONFIG
#
# Everything below is new with this theme. None of it is required - every
# variable falls back to a sensible default if absent - but set them to match
# the intent of the redesign prototype.
# =============================================================================

# --- Display name (separate from AUTHOR, which drives feeds/metadata) -------
# AUTHOR is kept as "Andy Wegner" for feed/metadata compatibility. The sidebar,
# nav wordmark, and author bio use AUTHOR_DISPLAY for the on-page name.
AUTHOR_DISPLAY = "Andrew Wegner"
AUTHOR_GIVEN = "Andrew"
AUTHOR_FAMILY = "Wegner"
AUTHOR_ROLE = "VP, Strategic Software"
AUTHOR_ROLE_LINES = [
    "VP,",
    "Strategic Software",
]  # stacked on two lines in the nav wordmark and sidebar

# --- Headshot -------------------------------------------------------------
HEADSHOT = "wegner_headshot.png"  # filename inside theme static/img/
HEADSHOT_MORPH = True  # True = morphing blob animation; False = still circle

# --- Contact / footer -------------------------------------------------------
CONTACT_EMAIL = "blog.feedback@andrewwegner.com"
RESUME_URL = "/resume.pdf"
RESUME_LABEL = "Download résumé (PDF)"
# Derived from CONTACT above but with display-friendly labels for the footer meta block:
SOCIAL_META = [
    ("LinkedIn", "https://www.linkedin.com/in/andrew-wegner/", "in/andrew-wegner"),
    ("GitHub", "https://github.com/AWegnerGitHub/", "@AWegnerGitHub"),
    (
        "Stack Overflow",
        "https://stackoverflow.com/users/189134/andy",
        "Elected moderator",
    ),
]

FOOTER_KICKER = "GET IN TOUCH"
FOOTER_HEADLINE = "Currently open to VP Engineering and CTO conversations."
FOOTER_SUB = (
    "I'm selective about what I take on, but always happy to talk about "
    "engineering leadership, distributed teams, and hiring."
)

# --- Home page sections -----------------------------------------------------
LANDING_HERO = {
    "kicker": "Engineering leader · Writer · Moderator",
    "headline": "Building the teams that <em>build the systems</em>.",
    "sub": (
        "I lead, grow and mentor engineering organizations across telecom, "
        "logistics and SaaS. Currently VP of Strategic Software at a "
        "telecommunications company. I write about what I've learned running "
        "distributed teams, managing technical debt, and hiring engineers in "
        "the age of AI."
    ),
    "primary_cta": {"url": "#writing", "label": "Read the latest essay"},
    "secondary_cta": {"url": "/archives.html", "label": "Browse all writing"},
    "meta": [
        ("Currently", "VP, Strategic Software"),
        ("Previously", "VP Eng · Director Eng"),
        ("Writing since", "2019"),
    ],
}

LANDING_METRICS = [
    ("40+", "Engineers in largest org led"),
    ("5", "Industries: telecom, logistics, hiring, manufacturing"),
    ("~20", "Years shipping software end-to-end"),
    ("3", "VP / Director engineering roles"),
]

LANDING_PRINCIPLES_HEAD = (
    "Four ideas that shape how I run engineering orgs.",
    "Drawn from fifteen years building teams across telecom, logistics, hiring "
    "and manufacturing. Each one has a corresponding essay.",
)

LANDING_PRINCIPLES = [
    # Each entry is (number, title, body) or (number, title, body, article_url).
    # If a 4th element is present and truthy, the whole card becomes a link to
    # that URL. Internal URLs starting with "/" get SITEURL prepended; full
    # URLs (https://...) are used verbatim. Omit the 4th element to render a
    # non-clickable card.
    (
        "01",
        "Distance doesn't diminish performance.",
        "Distributed teams outperform co-located ones when the operating model "
        "is designed for async decisions, written context, and clear ownership. "
        "Not transplanted from the office.",
    ),
    (
        "02",
        "Hire for what actually predicts the job.",
        "Most technical interviews measure test-taking under a stopwatch. I "
        "rebuild hiring around problem framing, trade-off articulation, and "
        "shipped evidence: the signals that correlate with on-the-job success.",
    ),
    (
        "03",
        "Technical debt is a leadership problem.",
        "Every team has debt. The ones that keep moving treat it as a portfolio "
        "(with explicit cost, interest, and a payback schedule), instead of a "
        "cleanup someone will get to someday.",
    ),
    (
        "04",
        "Grow engineers as the product.",
        "Mentorship and career ladders aren't HR overhead. They're the "
        "compounding investment. The output of an engineering org is the "
        "engineers it produces as much as the software it ships.",
    ),
]
