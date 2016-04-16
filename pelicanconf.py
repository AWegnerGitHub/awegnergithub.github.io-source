#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from pyembed.markdown import PyEmbedMarkdown

AUTHOR = u'Andy Wegner'
SITENAME = u'Ponderings of an Andy'
SITEURL = 'http://andrewwegner.com'
THEME = '../pelican-themes/elegant'
PLUGIN_PATHS = ['../pelican-plugins', 'plugins']
PLUGINS = ['neighbors', 'extract_toc', 'tipue_search', 'sitemap', 'keyboard.kb']
STATIC_PATHS = ['images', 'extra/CNAME']
MD_EXTENSIONS = ['codehilite(css_class=codehilite code)', 'toc(permalink=true)', 'mdx_video']
EXTRA_PATH_METADATA = {'extra\CNAME': {'path': 'CNAME'},}

PATH = 'content'

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = u'en'

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
SOCIAL = (('Stack Overflow', 'http://stackoverflow.com/users/189134/andy'),
          ('Steam', 'http://steamcommunity.com/id/InsaneMosquito/'),
          ('Stack Overflow Jobs', 'http://stackoverflow.com/cv/andrewwegner'))

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

LANDING_PAGE_ABOUT = {'title': """Can that be automated?""",
                      'details': """<div itemscope itemtype="http://schema.org/Person"><p>My name
        is <span itemprop="name">Andy Wegner</span>. </p><p>I work at a large manuafacturing company. I've build software
        that  covers pretty much every aspect of a product's life cycle: initial conception, design,
        manufacturing, transportation, field operations, warranty returns, repair and remanufacturing.</p>
        <p>I was the community owner of Team Vipers for 5 years. Vipers was a gaming community, focused mainly around
        Team Fortress 2, but we dabbled in other games for brief periods of time. I helped the community prosper. I also
        built a lot of software to help me in managing the community. </p>
        <p>I am active on <a href="http://stackoverflow.com/users/189134/andy">Stack Overflow</a> and the rest of the
        Stack Exchange network. I moderate <a href="http://communitybuilding.stackexchange.com/">Community Building</a> I've also
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