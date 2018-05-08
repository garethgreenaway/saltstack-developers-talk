# -*- coding: utf-8 -*-
'''
Module for controlling the Blinkt LED matrix

.. versionadded:: Fluorine

:maintainer:    Gareth J. Greenaway <gareth@saltstack.com>
:maturity:      new
:depends:       blinkt Python module

'''

from __future__ import absolute_import, unicode_literals, print_function

import colorsys
import logging
import time
import random

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
    else:
        return False, "The blinkt excecution module can not be loaded."


def random_colors():
    '''
    Set the LEDs to random colors

    CLI Example:

    .. code-block:: bash

        salt '*' blinkt.random_colors

    '''
    blinkt.set_clear_on_exit()
    blinkt.set_brightness(0.1)

    for i in range(blinkt.NUM_PIXELS):
        blinkt.set_pixel(i, random.randint(0, 255),
                         random.randint(0, 255),
                         random.randint(0, 255))
    blinkt.show()
    return {'result': True, 'comment': 'Set LEDs to random colors'}


def rainbow():
    '''
    Set the LEDs to the colors of the rainbow

    CLI Example:

    .. code-block:: bash

        salt '*' blinkt.rainbow

    '''
    spacing = 360.0 / 16.0
    hue = 0

    blinkt.set_clear_on_exit()
    blinkt.set_brightness(0.1)

    hue = int(time.time() * 100) % 360
    for x in range(blinkt.NUM_PIXELS):
        offset = x * spacing
        h = ((hue + offset) % 360) / 360.0
        r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
        blinkt.set_pixel(x, r, g, b)
    blinkt.show()
    return {'result': True, 'comment': 'Set LEDs to rainbow'}


def one_rgb(pixel=0, red=0, green=0, blue=0):
    '''
    Set the one LED to a color

    CLI Example:

    .. code-block:: bash

        salt '*' blinkt.one_rgb 5 255 120 10

    '''
    if pixel > blinkt.NUM_PIXELS:
        return False, 'Invalid pixel'

    blinkt.set_pixel(pixel, red, green, blue)
    blinkt.show()
    return {'result': True,
            'comment': 'Set pixel {0} to rgb ({1},{2},{3})'.format(pixel, red, green, blue)}


def range_rgb(start=0, end=1, red=255, green=255, blue=255):
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

    for pixel in range(start, end + 1):
        blinkt.set_pixel(pixel, red, green, blue)
        blinkt.show()
    return {'result': True,
            'comment': 'Set range {0}-{1} to rgb ({2},{3},{4})'.format(start, end, red, green, blue)}


def all_rgb(red=255, green=255, blue=255):
    '''
    Set all the LEDs to a color

    CLI Example:

    .. code-block:: bash

        salt '*' blinkt.all_rgb red=0 green=255 blue=0

    '''
    blinkt.set_all(red, green, blue)
    blinkt.show()
    return {'result': True,
            'comment': 'Set all pixels to rgb ({1},{2},{3})'.format(red, green, blue)}


def clear(**kwargs):
    '''
    Clear  one pixel, a range of pixels or all pixels

    CLI Example:

    .. code-block:: bash

        salt '*' blinkt.clear 5

        salt '*' blinkt.clear 3 5

        salt '*' blinkt.clear

    '''
    if 'pixel' in kwargs:
        ret = clear_one(kwargs['pixel'])
    elif 'start' in kwargs and 'end' in kwargs:
        ret = clear_range(kwargs['start'], kwargs['end'])
    else:
        blinkt.set_all(0, 0, 0)
        blinkt.show()
        comment = 'Clear all pixels'
        ret = {'result': True,
               'comment': comment}

    return ret


def clear_one(pixel):
    '''
    Clear one pixel

    CLI Example:

    .. code-block:: bash

        salt '*' blinkt.clear_one 5

    '''
    blinkt.set_pixel(pixel, 0, 0, 0)
    blinkt.show()
    comment = 'Clear pixel {0}'.format(pixel)
    return {'result': True,
            'comment': comment}


def clear_range(start_pixel, end_pixel):
    '''
    Clear one pixel

    CLI Example:

    .. code-block:: bash

        salt '*' blinkt.clear_range 2 6

    '''
    for pixel in range(start_pixel, end_pixel + 1):
        blinkt.set_pixel(pixel, 0, 0, 0)
    blinkt.show()
    comment = 'Clear pixel range {0}-{1}'.format(start_pixel, end_pixel)
    return {'result': True,
            'comment': comment}
