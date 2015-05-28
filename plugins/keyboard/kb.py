# Source: http://nafiulis.me/making-a-static-blog-with-pelican.html#plugins

from pelican import signals

import logging
import re

logging.Logger(__name__)


def content_object_init(instance):
    """
    Provides the key plugin, make sure that you have Keys.css, http://michaelhue.com/keyscss/
    imported inside your HTML. How to use:

        So you hit [kb:CTRL] + [kb:ALT] + [kb:DEL] when in doubt

    Note, that light keyboard keys are enabled by default.
    """
    if instance._content is not None:
        content = instance._content
        new_content = re.sub(r"\[kb:(.+?)\]", r'<kbd class="light">\1</kbd>', content)
        instance._content = new_content
        return instance


def register():
    signals.content_object_init.connect(content_object_init)