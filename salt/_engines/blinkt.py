# -*- coding: utf-8 -*-
'''
Engine for controlling the Blinkt LED matrix

.. versionadded:: Fluorine

:maintainer:    Gareth J. Greenaway <gareth@saltstack.com>
:maturity:      new
:depends:       blinkt Python module

'''

# Import python libs
from __future__ import absolute_import, print_function, unicode_literals
import datetime
import colorsys
import logging
import random
import time

try:
    import blinkt
    HAS_BLINKT = True
except (ImportError, NameError):
    HAS_BLINKT = False

# Import salt libs
import salt.utils.event

log = logging.getLogger(__name__)

def __virtual__():
    '''
    Only load the module if Blinkt is available
    '''
    if HAS_BLINKT:
        return True
    return False

class BlinktEngine(object):
    '''
    Blinkt engine
    '''
    def __init__(self):
        self.stop_time = None

    def run(self):
        '''
        Main loop function
        '''
        if __opts__['__role'] == 'master':
            event_bus = salt.utils.event.get_master_event(
                __opts__,
                __opts__['sock_dir'],
                listen=True)
        else:
            event_bus = salt.utils.event.get_event(
                'minion',
                transport=__opts__['transport'],
                opts=__opts__,
                sock_dir=__opts__['sock_dir'],
                listen=True)

        _kwargs = {}
        mode = None
        while True:
            now = datetime.datetime.now()
            event = event_bus.get_event(full=True)
            if event:
                if 'tag' in event:
                    if event['tag'].startswith('/salt/minion/blinkt'):
                        mode = event['data'].get('mode', None)
                        _kwargs = event['data'].get('kwargs', {})
                        if _kwargs.get('timeout', None):
                            self.stop_time = now + datetime.timedelta(seconds=_kwargs.get('timeout'))

            if mode:
                func = getattr(self, mode, None)
                if func:
                    func(**_kwargs)
                    if self.stop_time:
                        if self.stop_time <= now:
                            mode = None
                            self.clear(**_kwargs)

    def random_blink_colors(self, **kwargs):
        '''
        Set the LEDs to random colors
        '''
        blinkt.set_clear_on_exit()
        blinkt.set_brightness(0.1)

        for i in range(blinkt.NUM_PIXELS):
            blinkt.set_pixel(i, random.randint(0, 255),
                             random.randint(0, 255), random.randint(0, 255))
        blinkt.show()

    def rainbow(self, **kwargs):
        '''
        Set the LEDs to the colors of the rainbow
        '''

        spacing = 360.0 / 16.0
        hue = 0

        blinkt.set_clear_on_exit()
        blinkt.set_brightness(0.1)

        hue = int(time.time() * 100) % 360
        for x in range(blinkt.NUM_PIXELS):
            offset = x * spacing
            h = ((hue + offset) % 360) / 360.0
            red, green, blue = [int(c*255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            blinkt.set_pixel(x, red, green, blue)
        blinkt.show()

    def one_rgb(self, **kwargs):
        '''
        Set the one LED to a color
        '''
        pixel = kwargs.get('pixel')
        red = kwargs.get('red')
        green = kwargs.get('green')
        blue = kwargs.get('blue')
        blinkt.set_pixel(pixel, red, green, blue)
        blinkt.show()

    def range_rgb(self, **kwargs):
        '''
        Set a range of LEDs to a color
        '''
        start_pixel = kwargs.get('start_pixel')
        end_pixel = kwargs.get('end_pixel')
        red = kwargs.get('red')
        green = kwargs.get('green')
        blue = kwargs.get('blue')
        for pixel in range(start_pixel, end_pixel + 1):
            blinkt.set_pixel(pixel, red, green, blue)
            blinkt.show()

    def all_rgb(self, **kwargs):
        '''
        Set all the LEDs to a color
        '''
        red = kwargs.get('red')
        green = kwargs.get('green')
        blue = kwargs.get('blue')
        blinkt.set_all(r, g, b)
        blinkt.show()

    def clear(self, **kwargs):
        '''
        Clear one pixel, a range of pixels or all pixels
        '''
        if 'pixel' in kwargs:
            self.clear_one(kwargs['pixel'])
        elif 'start' in kwargs and 'end' in kwargs:
            self.clear_range(kwargs['start'], kwargs['end'])
        else:
            blinkt.set_all(0, 0, 0)
            blinkt.show()

    def clear_one(self, pixel):
        '''
        Clear one pixel
        '''
        blinkt.set_pixel(pixel, 0, 0, 0)
        blinkt.show()

    def clear_range(self, start_pixel, end_pixel):
        '''
        Clear range of pixels
        '''
        for pixel in range(start_pixel, end_pixel + 1):
            blinkt.set_pixel(pixel, 0, 0, 0)
        blinkt.show()

def start(interval=1):
    '''
    Listen to events and write them to a log file
    '''
    client = BlinktEngine()
    client.run()
