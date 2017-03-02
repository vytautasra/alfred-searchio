#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2016 Dean Jackson <deanishe@deanishe.net>
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2016-12-17
#

"""searchio config [<query>]

Display (and optionally filter) workflow configuration
options.

Usage:
    searchio config [<query>]
    searchio config -h

Options:
    -h, --help     Display this help message
"""

from __future__ import print_function, absolute_import

from operator import itemgetter

from docopt import docopt

from workflow import (
    # ICON_SETTINGS,
    ICON_WARNING,
)

from searchio.core import Context
# from searchio.engines import Manager as EngineManager
from searchio import util

log = util.logger(__name__)


def usage(wf=None):
    """CLI usage instructions."""
    return __doc__


def run(wf, argv):
    """Run ``searchio list`` sub-command."""
    ctx = Context(wf)
    ICON_UPDATE_AVAILABLE = ctx.icon('update-available')
    ICON_UPDATE_NONE = ctx.icon('update-none')
    ICON_HELP = ctx.icon('help')
    ICON_RELOAD = ctx.icon('reload')

    args = docopt(usage(wf), argv)

    log.debug('args=%r', args)
    query = wf.decode(args.get('<query>') or '').strip()

    # ---------------------------------------------------------
    # Configuration items

    items = []

    if wf.update_available:
        items.append(dict(
            title=u'Update Available \U00002026',
            subtitle=u'Action to install now',
            autocomplete=u'workflow:update',
            valid=False,
            icon=ICON_UPDATE_AVAILABLE,
        ))

    # items.append(dict(
    #     title=title,
    #     subtitle=subtitle,
    #     autocomplete=u'workflow:update',
    #     valid=False,
    #     icon=icon,
    # ))

    items.append(dict(
        title=u'User Engines \U00002026',
        subtitle=u'Your own engines',
        arg=u'user',
        valid=True,
        icon=u'icon.png',
    ))

    items.append(dict(
        title=u'All Engines \U00002026',
        subtitle=u'Browse supported engines',
        arg=u'engines',
        valid=True,
        icon=u'icon.png',
    ))

    items.append(dict(
        title=u'Online Help',
        subtitle=u'Open the help page in your browser',
        arg=u'help',
        valid=True,
        # autocomplete=u'workflow:help',
        # valid=False,
        icon=ICON_HELP,
    ))

    items.append(dict(
        title=u'Reload',
        subtitle=u'Re-create your searches',
        arg=u'reload',
        valid=True,
        # autocomplete=u'workflow:help',
        # valid=False,
        icon=ICON_RELOAD,
    ))

    if not wf.update_available:
        items.append(dict(
            title=u'Workflow up to Date',
            subtitle=u'Action to check for a newer version now',
            autocomplete=u'workflow:update',
            valid=False,
            icon=ICON_UPDATE_NONE,
        ))

    # ---------------------------------------------------------
    # Show results

    if query:
        items = wf.filter(query, items, key=itemgetter('title'))

    if not items:
        wf.add_item('No matching items',
                    'Try a different query?',
                    icon=ICON_WARNING)

    for d in items:
        wf.add_item(**d)

    wf.send_feedback()
    return
