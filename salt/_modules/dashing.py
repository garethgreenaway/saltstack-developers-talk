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
    Get Dashing configuration
    '''
    return __salt__['config.get']('dashing.url') or \
        __salt__['config.get']('dashing:url')


def _get_token():
    '''
    Retrieve Dashing Token
    '''
    return __salt__['config.get']('dashing.token') or \
        __salt__['config.get']('dashing:token')


def _query(function,
           dashing_url,
           token=None,
           method='GET',
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


def widget_post(dashing_url=None,
                token=None,
                widget=None,
                widget_data=None):
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

    Reload the Dashing dashboard

    :param dashing_url: The Dashing server URL.
    :param token: The token to use.
    :return: True

    CLI Example:

    .. code-block:: bash

        salt '*' dashing.wdget_post dashing_url="http://localhost:3030" token="YOUR_AUTH_TOKEN" widget="widget_name" widget_data="{'key': 'value'}"

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
