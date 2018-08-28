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
import urllib

# Import salt libs
import salt.utils.event

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
        self.stop_times = {}

    def _get_config(self):
        '''
        Retrieve Consul configuration
        '''
        return __salt__['config.get']('dashing.url') or \
            __salt__['config.get']('dashing:url')

    def _get_token(self):
        '''
        Retrieve Consul configuration
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
        Consul object method function to construct and execute on the API URL.

        :param api_url:     The Consul api url.
        :param api_version  The Consul api version
        :param function:    The Consul api function to perform.
        :param method:      The HTTP method, e.g. GET or POST.
        :param data:        The data to be sent for POST method. This param is ignored for GET requests.
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
        while True:
            now = datetime.datetime.now()
            event = event_bus.get_event(full=True)
            if event:
                if 'tag' in event:
                    if event['tag'].startswith('/salt/minion/dashing'):
                        _kwargs = event['data'].get('kwargs', {})
                        if _kwargs.get('timeout', None):
                            self.stop_time = now + datetime.timedelta(seconds=_kwargs.get('timeout'))

                            for widget in _kwargs.get('widget_data', {}):
                                self.stop_times[widget] = now + datetime.timedelta(seconds=_kwargs.get('timeout'))

                        self.widget_post(**_kwargs)

            for widget in self.stop_times:
                log.debug(self.stop_times[widget])
                if self.stop_times[widget]:
                    if self.stop_times[widget] <= now:
                        self.clear(widget=_kwargs['widget'],
                                   widget_data={widget: '1'})
                        self.stop_times[widget] = None

    def widget_post(self,
                    dashing_url=None,
                    token=None,
                    widget=None,
                    widget_data=None,
                    **kwargs):
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
        log.debug(kwargs)
        self.widget_post(**kwargs)


def start(interval=1):
    '''
    Listen to events and write them to a log file
    '''
    client = DashingEngine()
    client.run()
