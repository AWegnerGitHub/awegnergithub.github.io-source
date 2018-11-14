#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from pyembed.markdown import PyEmbedMarkdown

AUTHOR = u'Andy Wegner'
SITENAME = u'Ponderings of an Andy'
SITEURL = 'https://andrewwegner.com'
THEME = 'pelican-themes/elegant'
PLUGIN_PATHS = ['../pelican-plugins', 'plugins']
# https://pypi.python.org/pypi/pelican-extended-sitemap
PLUGINS = ['neighbors', 'extract_toc', 'tipue_search', 'extended_sitemap', 'keyboard.kb', 'series', 'post_stats']
MARKDOWN = {'extension_configs': {
    'markdown.extensions.codehilite': {'css_class': 'codehilight code'},
    'markdown.extensions.toc': {'permalink': 'true'},
    'mdx_video': {}
}
}
STATIC_PATHS = ['images', 'extra/CNAME', 'extra/google8e079521c0d93c27.html', "extra/robots.txt", "extra/keybase.txt"]
EXTRA_PATH_METADATA = {r'extra/CNAME': {'path': 'CNAME'},
                       r'extra/google8e079521c0d93c27.html': {'path': 'google8e079521c0d93c27.html'},
                       r'extra/robots.txt': {'path': 'robots.txt'},
                       r'extra/keybase.txt': {'path': 'keybase.txt'},
                       }

PATH = 'content'

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = u'en'
READERS = {'html': None}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('Stack Overflow', 'https://stackoverflow.com/users/189134/andy', 'stack-overflow'),
          ('Steam', 'http://steamcommunity.com/id/InsaneMosquito/', 'steam-square'),
          ('Stack Overflow Jobs', 'https://stackoverflow.com/cv/andrewwegner', 'stack-overflow'))

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

LANDING_PAGE_ABOUT = {'title': """Can that be automated?""",
                      'details': """<div itemscope itemtype="https://schema.org/Person"><p>My name
        is <span itemprop="name">Andy Wegner</span>. </p><p>I am a Product Reliability Engineer at a small company.
		I've worked at a large manuafacturing company building software that  covers pretty much every aspect of a product's life 
		cycle: initial conception, design, manufacturing, transportation, field operations, warranty returns, repair and remanufacturing.</p>
        <p>I was the community owner of Team Vipers for 5 years. Vipers was a gaming community, focused mainly around
        Team Fortress 2, but we dabbled in other games for brief periods of time. I helped the community prosper. I also
        built a lot of software to help me in managing the community. </p>
        <p>I am active on <a href="https://stackoverflow.com/users/189134/andy">Stack Overflow</a> and the rest of the
        Stack Exchange network. I moderate <a href="https://communitybuilding.stackexchange.com/">Community Building</a> and
		<a href="https://hardwarerecs.stackexchange.com/">Hardware Recommendations</a>. I've also
        built a few tools to help keep the low quality content off the Stack Exchange network.</p></div>"""
                      }

PROJECTS = [
    {
        'name': 'StackAPI',
        'url': 'https://github.com/AWegnerGitHub/stackapi',
        'description': 'A Python wrapper for the Stack Exchange API.'
    },
    {
        'name': 'Zephyr - Vote Request Bot',
        'url': 'https://github.com/AWegnerGitHub/SE_Zephyr_VoteRequest_bot',
        'description': 'Zephyr is a headless chatbot that monitors chat rooms on the Stack Exchange network for vote requests from other users and posts them to a specified room.'
    },
    {
        'name': 'IRVING',
        'url': 'https://github.com/AWegnerGitHub/IRVING',
        'description': 'IRVING is a system built to integrate directly with end user systems. Users know their data and they know the conditions that are abnormal and worth monitoring. IRVING allows users to set up a customized dashboard to monitor their important data points through multiple systems.'
    },
    {
        'name': 'AndrewWegner.com',
        'url': 'https://github.com/AWegnerGitHub/awegnergithub.github.io-source',
        'description': 'The source for this blog'
    },
    {
        'name': 'Team Vipers Game Server Plugins',
        'url': 'https://github.com/AWegnerGitHub/Vipers-Server-Plugins',
        'description': 'Custom SourceMod plugins built for the Team Vipers community'
    },

]

EXTENDED_SITEMAP_PLUGIN = {
    'priorities': {
        'index': 1.0,
        'articles': 0.8,
        'pages': 0.5,
        'others': 0.4
    },
    'changefrequencies': {
        'index': 'daily',
        'articles': 'weekly',
        'pages': 'weekly',
        'others': 'monthly',
    }
}

FONT_AWESOME_EMBED_CODE = 'e4a49a2d36'
AUTHORS = {
    u'Andy Wegner': {
        u'image': 'wegner_headshot.png',
        u'blurb': """ is a father, an engineer and a computer scientist. He is interested in online 
            community building, tinkering with new code and building new applications. 
            He writes about his experiences with each of these.""",
        u'friendly_name': "Andy Wegner",
        u'url': 'https://andrewwegner.com/'

    }

}
