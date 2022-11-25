import datetime

AUTHOR = "Andy Wegner"
SITENAME = "Ponderings of an Andy"
SITEURL = "https://andrewwegner.com"
# SITEURL = ""
SITESUBTITLE = "Can that be automated?"
SITEDESCRIPTION = "Articles and reviews covering thoughts on work place leadership, technical course reviews, and other ponderings of Andy"
COPYRIGHT_YEAR = datetime.date.today().year
COPYRIGHT_NAME = "Andrew Wegner"
SITELOGO = "/images/wegner_headshot.png"


PATH = "content"
READERS = {"html": None}
THEME = "flex"
OUTPUT_PATH = "output/"

TIMEZONE = "America/Chicago"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["series", "extract_toc", "neighbors", "keyboard", "extended_sitemap"]

TOC = {"TOC_HEADERS": "^h[1-3]"}

MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "codehilight code"},
        "markdown.extensions.toc": {"permalink": "true"},
        "customblocks": {},
    }
}

JINJA_ENVIRONMENT = {"extensions": ["jinja2.ext.do"]}


DISPLAY_PAGES_ON_MENU = False
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
# Blogroll
LINKS = (
    ("Home", "/"),
    ("About Me", "/about"),
    ("Archives", "/archives.html"),
    ("Categories", "/categories.html"),
    ("Tags", "/tags.html"),
)

# Social widget
CONTACT = (
    ("linkedin", "https://www.linkedin.com/in/andrew-wegner/", "andy-linkedin"),
    ("stack-overflow", "https://stackoverflow.com/users/189134/andy", "andy-stackoverflow"),
    ("github", "https://github.com/AWegnerGitHub/", "andy-github"),
    ("file-pdf", "/resume.pdf", "andy-resume"),
    ("envelope", "mailto:blog.feedback@andrewwegner.com", "andy-blogemail"),
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
DISABLE_URL_HASH = True
SHOW_CONTINUE_READING_BUTTON = False

TAG_GRAPH = True
CATEGORY_GRAPH = True

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True


AUTHORS = {
    u"Andy Wegner": {
        u"image": "wegner_headshot.png",
        u"blurb": """ is a father, an engineer and a computer scientist. He is interested in online
            community building, tinkering with new code and building new applications.
            He writes about his experiences with each of these.""",
        u"friendly_name": "Andy Wegner",
        u"url": "https://andrewwegner.com/",
    }
}

REVIEW_PROVIDERS = {
    "Udemy": {"type": "Organization", "name": "Udemy", "sameAs": "https://www.udemy.com/", "itemType": "Course"},
    "Coursera": {
        "type": "Organization",
        "name": "Coursera",
        "sameAs": "https://www.coursera.org/",
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
    "changefrequencies": {"index": "daily", "articles": "weekly", "pages": "weekly", "others": "monthly"},
}

LANDING_PAGE_ABOUT = """<div><p>My name
        is <span class="itsme">Andy Wegner</span>.</p><p>I lead, grow and mentor engineering teams in many industries. 
        I've worked as VP of Software Engineering at a telecommunications company, Director of Engineering at a transportation
        logistics company and at a company working to improve the hiring process for engineers. I've been an individual contributor 
        at a large manuafacturing company.
        I've built global teams of engineers and delivered solutions that impact customers worldwide.
        I've personally built software that covers much every aspect of a product's lifecycle in multiple industries.</p>
        <p>I was the community owner of Team Vipers for 5 years. Vipers was a gaming community, focused mainly around
        Team Fortress 2, but we dabbled in other games for brief periods of time. I helped the community prosper. I also
        built a lot of software to help me in managing the community. </p>
        <p>I am an elected Moderator on <a href="https://stackoverflow.com/users/189134/andy">Stack Overflow</a> and participate across the rest of the
        Stack Exchange network. I moderate <a href="https://communitybuilding.stackexchange.com/">Community Building</a> and
        <a href="https://hardwarerecs.stackexchange.com/">Hardware Recommendations</a> as well. I've also
        built a few tools to help keep the low quality content off the Stack Exchange network.</p></div>"""


HEAP_ANALYTICS = 653100411
BROWSER_COLOR = "#080019"
FAVICON = "/favicon.ico"
APPLETOUCHICON = "/apple-touch-icon.png"
FAVICON32X32 = "/favicon-32x32.png"
FAVICON16X16 = "/favicon-16x16.png"
SITEMANIFEST = "/site.webmanifest"
