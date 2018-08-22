# -*- coding: utf-8 -*-
'''
Module for controlling the Blinkt LED matrix

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
    Get key from Consul

    :param consul_url: The Consul server URL.
    :param key: The key to use as the starting point for the list.
    :param recurse: Return values recursively beginning at the value of key.
    :param decode: By default values are stored as Base64 encoded values,
                   decode will return the whole key with the value decoded.
    :param raw: Simply return the decoded value of the key.
    :return: The keys in Consul.

    CLI Example:

    .. code-block:: bash

        salt '*' consul.get key='web/key1'
        salt '*' consul.get key='web' recurse=True
        salt '*' consul.get key='web' recurse=True decode=True

    By default values stored in Consul are base64 encoded, passing the
    decode option will show them as the decoded values.

    .. code-block:: bash

        salt '*' consul.get key='web' recurse=True decode=True raw=True

    By default Consult will return other information about the key, the raw
    option will return only the raw value.

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
