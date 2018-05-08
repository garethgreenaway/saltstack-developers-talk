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

__virtualname__ = 'blinkt'

try:
    import blinkt
    HAS_BLINKT = True
except (ImportError, NameError):
    HAS_BLINKT = False
log = logging.getLogger(__name__)


def __virtual__():
    '''
    Only load the module if Blinkt is available
    '''
    if HAS_BLINKT:
        return __virtualname__
    return False, "The blinkt excecution module can not be loaded."


def random_colors(timeout=None):
    '''
    Set the LEDs to random colors

    CLI Example:

    .. code-block:: bash

        salt '*' blinkt.random_colors

    '''
    try:
        res = __salt__['event.fire']({'mode': 'random_blink_colors',
                                      'kwargs': {'timeout': timeout}},
                                     '/salt/minion/blinkt')
        ret = {'result': True, 'comment': 'Set LEDs to random colors'}
    except KeyError:
        # Effectively a no-op, since we can't really return without an event system
        ret = {}
        ret['comment'] = 'Event module not available.'
        ret['result'] = True
    return ret


def rainbow(timeout=None):
    '''
    Set the LEDs to the colors of the rainbow

    CLI Example:

    .. code-block:: bash

        salt '*' blinkt.rainbow

    '''
    try:
        res = __salt__['event.fire']({'mode': 'rainbow',
                                      'kwargs': {'timeout': timeout}},
                                     '/salt/minion/blinkt')
        ret = {'result': True, 'comment': 'Set LEDs to rainbow'}
    except KeyError:
        # Effectively a no-op, since we can't really return without an event system
        ret = {}
        ret['comment'] = 'Event module not available.'
        ret['result'] = True
    return ret


def one_rgb(pixel=0, red=0, green=0, blue=0, timeout=None):
    '''
    Set the one LED to a color

    CLI Example:

    .. code-block:: bash

        salt '*' blinkt.one_rgb 5 255 120 10

    '''
    if pixel > blinkt.NUM_PIXELS:
        return False, 'Invalid pixel'

    try:
        res = __salt__['event.fire']({'mode': 'one_rgb',
                                      'kwargs': {'pixel': pixel,
                                                 'red': red,
                                                 'green': green,
                                                 'blue': blue,
                                                 'timeout': timeout}},
                                     '/salt/minion/blinkt')
        ret = {'result': True,
               'comment': 'Set pixel {0} to rgb ({1},{2},{3})'.format(pixel, red, green, blue)}
    except KeyError:
        # Effectively a no-op, since we can't really return without an event system
        ret = {}
        ret['comment'] = 'Event module not available.'
        ret['result'] = True
    return ret


def range_rgb(start=0, end=1, red=255, green=255, blue=255, timeout=None):
    '''
    Set a range of LEDs to a color

    CLI Example:

    .. code-block:: bash

        salt '*' blinkt.range_rgb start=2 end=5 red=0 green=255 blue=0

    '''
    if start > blinkt.NUM_PIXELS:
        return False, 'Invalid start pixel'

    if end > blinkt.NUM_PIXELS:
        return False, 'Invalid end pixel'

    try:
        res = __salt__['event.fire']({'mode': 'range_rgb',
                                      'kwargs': {'start_pixel': start,
                                                 'end_pixel': end,
                                                 'red': red,
                                                 'green': green,
                                                 'blue': blue,
                                                 'timeout': timeout}},
                                     '/salt/minion/blinkt')
        ret = {'result': True,
               'comment': 'Set range {0}-{1} to rgb ({2},{3},{4})'.format(start, end, red, green, blue)}
    except KeyError:
        # Effectively a no-op, since we can't really return without an event system
        ret = {}
        ret['comment'] = 'Event module not available.'
        ret['result'] = True
    return ret


def all_rgb(red=255, green=255, blue=255, timeout=None):
    '''
    Set all the LEDs to a color

    CLI Example:

    .. code-block:: bash

        salt '*' blinkt.all_rgb red=0 green=255 blue=0

    '''
    try:
        res = __salt__['event.fire']({'mode': 'all_rgb',
                                      'kwargs': {'red': red,
                                                 'green': green,
                                                 'blue': blue,
                                                 'timeout': timeout}},
                                     '/salt/minion/blinkt')
        ret = {'result': True,
               'comment': 'Set all pixels to rgb ({1},{2},{3})'.format(red, green, blue)}
    except KeyError:
        # Effectively a no-op, since we can't really return without an event system
        ret['comment'] = 'Event module not available.'
        ret['result'] = True
    return ret


def clear(**kwargs):
    '''
    Clear  one pixel, a range of pixels or all pixels

    CLI Example:

    .. code-block:: bash

        salt '*' blinkt.clear 5

        salt '*' blinkt.clear 3 5

        salt '*' blinkt.clear

    '''
    try:
        res = __salt__['event.fire']({'mode': 'clear', 'kwargs': kwargs}, '/salt/minion/blinkt')

        if 'pixel' in kwargs:
            comment = 'Clear pixel {0}'.format(kwargs['pixel'])
        elif 'start' in kwargs and 'end' in kwargs:
            comment = 'Clear pixel range {0}-{1}'.format(start_pixel, end_pixel)
        else:
            comment = 'Clear all pixels'

        ret = {'result': True,
               'comment': comment}

    except KeyError:
        # Effectively a no-op, since we can't really return without an event system
        ret = {}
        ret['comment'] = 'Event module not available.'
        ret['result'] = True

    return ret
