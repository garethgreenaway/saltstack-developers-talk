# -*- coding: utf-8 -*-
'''
Engine for controlling Dashing

.. versionadded:: Fluorine

:maintainer:    Gareth J. Greenaway <gareth@saltstack.com>
:maturity:      new

'''

# Import python libs
from __future__ import absolute_import, print_function, unicode_literals
import datetime
import logging


# Import salt libs
import salt.utils.event
from salt.ext import six
from salt.ext.six.moves import http_client, urllib

log = logging.getLogger(__name__)


def __virtual__():
    '''
    Only load the module if Blinkt is available
    '''
    return True


class DashingEngine(object):
    '''
    Dashing engine
    '''
    def __init__(self):
        self.stop_time = None

    def _get_config(self):
        '''
        Get Dashing configuration
        '''
        return __salt__['config.get']('dashing.url') or \
            __salt__['config.get']('dashing:url')

    def _get_token(self):
        '''
        Get Dashing token
        '''
        return __salt__['config.get']('dashing.token') or \
            __salt__['config.get']('dashing:token')

    def _query(self,
               function,
               dashing_url,
               token=None,
               method='GET',
               api_version='v1',
               data=None,
               query_params=None):
        '''
        Private query function for calling Dashing URL

        :param dashing_url: The Dashing api url.
        :param token        The Dashing tokne
        :param function:    The Dashing function to perform.
        :param method:      The HTTP method, e.g. GET or POST.
        :param data:        The data to be sent for POST method. This param is ignored for GET requests.
        :param query_params:  Additional query params.
        :return:            The json response from the API call or False.
            '''

        if not query_params:
            query_params = {}

        ret = {'data': '',
               'res': True}

        headers = {"auth_token": token, "Content-Type": "application/json"}
        url = urllib.parse.urljoin(dashing_url, function, False)

        if method == 'GET':
            data = None
        else:
            if data is None:
                data = {}
            data = salt.utils.json.dumps(data)

        result = salt.utils.http.query(
            url,
            method=method,
            params=query_params,
            data=data,
            decode=False,
            status=True,
            header_dict=headers,
            opts=__opts__,
        )

        return ret

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
        post = None
        while True:
            now = datetime.datetime.now()
            event = event_bus.get_event(full=True)
            if event:
                if 'tag' in event:
                    if event['tag'].startswith('/salt/minion/dashing'):
                        post = True
                        _kwargs = event['data'].get('kwargs', {})
                        if _kwargs.get('timeout', None):
                            self.stop_time = now + datetime.timedelta(seconds=_kwargs.get('timeout'))

            if post:
                self.widget_post(**_kwargs)
                if self.stop_time:
                    if self.stop_time <= now:
                        self.clear(**_kwargs)
                        post = None
                else:
                    post = None

    def widget_post(self,
                    dashing_url=None,
                    token=None,
                    widget=None,
                    widget_data=None,
                    **kwargs):
        '''
        Post data a Dashing widget

        :param dashing_url: The Dashing server URL.
        :param token: The token to use.
        :param widget:  The widget to post data to
        :param widget_data: The data to post to the widget.
        :return: True

        '''
        ret = {}
        if not dashing_url:
            dashing_url = self._get_config()
            if not dashing_url:
                log.error('No Dashing URL found.')
                ret['message'] = 'No Dashing URL found.'
                ret['res'] = False
                return ret

        if not token:
            token = self._get_token()

        data = {}
        data['auth_token'] = token
        data.update(widget_data)
        function = 'widgets/{0}'.format(widget)
        ret = self._query(dashing_url=dashing_url,
                          function=function,
                          method='POST',
                          token=token,
                          data=data)
        return ret

    def clear(self, **kwargs):
        '''
        Clear one pixel, a range of pixels or all pixels
        '''
        if 'widget_data' in kwargs:
            for key in kwargs['widget_data']:
                kwargs['widget_data'][key] = 1
        self.widget_post(**kwargs)


def start(interval=1):
    '''
    Listen to events and write them to a log file
    '''
    client = DashingEngine()
    client.run()
