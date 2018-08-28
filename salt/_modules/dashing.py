# -*- coding: utf-8 -*-
'''
Interact with a Dashing dashboard

'''

# Import Python Libs
from __future__ import absolute_import, print_function, unicode_literals
import base64
import logging

# Import salt libs
import salt.utils.http
import salt.utils.json

# Import 3rd-party libs
from salt.ext import six
from salt.ext.six.moves import http_client, urllib

log = logging.getLogger(__name__)

from salt.exceptions import SaltInvocationError

# Don't shadow built-ins.
__func_alias__ = {
    'list_': 'list'
}

__virtualname__ = 'dashing'


def _get_config():
    '''
    Retrieve Consul configuration
    '''
    return __salt__['config.get']('dashing.url') or \
        __salt__['config.get']('dashing:url')


def _get_token():
    '''
    Retrieve Consul configuration
    '''
    return __salt__['config.get']('dashing.token') or \
        __salt__['config.get']('dashing:token')


def _query(function,
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


def widget_post(dashing_url=None,
                token=None,
                widget=None,
                widget_data=None):
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
        dashing_url = _get_config()
        if not dashing_url:
            log.error('No Dashing URL found.')
            ret['message'] = 'No Dashing URL found.'
            ret['res'] = False
            return ret

    if not token:
        token = _get_token()

    data = {}
    data['auth_token'] = token
    data.update(widget_data)
    function = 'widgets/{0}'.format(widget)
    ret = _query(dashing_url=dashing_url,
                 function=function,
                 method='POST',
                 token=token,
                 data=data)
    return ret


def dashboard_reload(dashing_url=None,
                     token=None):
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
        dashing_url = _get_config()
        if not dashing_url:
            log.error('No Dashing URL found.')
            ret['message'] = 'No Dashing URL found.'
            ret['res'] = False
            return ret

    data = {}
    data['auth_token'] = token
    data['event'] = 'reload'
    function = 'dashboards/*'
    ret = _query(dashing_url=dashing_url,
                 function=function,
                 method='POST',
                 token=token,
                 data=data)
    return ret
