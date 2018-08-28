# -*- coding: utf-8 -*-
'''
Interact with a Dashing dashboard

.. versionadded:: Fluorine

:maintainer:    Gareth J. Greenaway <gareth@saltstack.com>
:maturity:      new
:depends:       blinkt Python module

'''

from __future__ import absolute_import, unicode_literals, print_function

import logging

log = logging.getLogger(__name__)


def __virtual__():
    '''
    Only load the module if Blinkt is available
    '''
    return True


def widget_post(**kwargs):
    '''
    Post data a Dashing widget

    :param dashing_url: The Dashing server URL.
    :param token: The token to use.
    :param widget:  The widget to post data to
    :param widget_data: The data to post to the widget.
    :return: True

    CLI Example:

    .. code-block:: bash

        salt '*' dashing.wdget_post dashing_url="http://localhost:3030" token="YOUR_AUTH_TOKEN" widget="widget_name" widget_data="{'key': 'value'}"

    '''
    try:
        res = __salt__['event.fire']({'kwargs': kwargs},
                                     '/salt/minion/dashing')
        ret = {'result': True, 'comment': 'Updated dashing widget'}
    except KeyError:
        # Effectively a no-op, since we can't really return without an event system
        ret = {}
        ret['comment'] = 'Event module not available.'
        ret['result'] = True
    return ret
