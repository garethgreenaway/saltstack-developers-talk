# -*- coding: utf-8 -*-
'''
Query the  StarWars API

https://swapi.co/

.. versionadded:: Fluorine

'''

# Import python libs
from __future__ import absolute_import, print_function, unicode_literals
import logging

# Import salt libs
from salt.exceptions import SaltInvocationError
import salt.utils.http
import salt.utils.json

log = logging.getLogger(__name__)


def __virtual__():
    '''
    load the module
    '''
    return True


def _query(action=None,
           id_key=None,
           args=None,
           method='GET',
           header_dict=None,
           data=None):
    '''
    Make a web call to the SWAPI
    '''
    path = 'https://swapi.co/api/'

    if action:
        path += '{0}/'.format(action)

    if id_key:
        path += '{0}/'.format(id_key)

    log.debug('SWAPI URL: %s', path)

    if not isinstance(args, dict):
        args = {}

    if header_dict is None:
        header_dict = {'Content-type': 'application/json'}

    if method != 'POST':
        header_dict['Accept'] = 'application/json'

    decode = True

    result = salt.utils.http.query(
        path,
        method,
        params=args,
        data=data,
        header_dict=header_dict,
        decode=decode,
        decode_type='json',
        text=True,
        status=True,
        cookies=True,
        persist_session=True,
        opts=__opts__,
    )
    if 'error' in result:
        log.error(result['error'])
        return [result['status'], result['error']]

    return [result['status'], result.get('dict', {})]


def people(id_key=None, **kwargs):
    '''
    Query Star Wars people

    CLI Example:

    .. code-block:: bash

        salt '*' swapi.people

        salt '*' swapi.people 1

    '''

    status, result = _query(action='people',
                            id_key=id_key,
                            method='GET')
    if 'films' in result:
        _films = []
        for film in result['films']:
            film_id = film[-2]
            film_name = films(film_id)['title']
            _films.append(film_name)
        result['films'] = _films
    return result


def films(id_key=None, **kwargs):
    '''
    Query Star Wars films

    CLI Example:

    .. code-block:: bash

        salt '*' swapi.films

        salt '*' swapi.films 1

    '''

    status, result = _query(action='films',
                            id_key=id_key,
                            method='GET')
    return result


def planets(id_key=None, **kwargs):
    '''
    Query Star Wars planets

    CLI Example:

    .. code-block:: bash

        salt '*' swapi.films

        salt '*' swapi.films 1

    '''

    status, result = _query(action='planets',
                            id_key=id_key,
                            method='GET')
    return result


def spaceships(id_key=None, **kwargs):
    '''
    Query Star Wars spaceships

    CLI Example:

    .. code-block:: bash

        salt '*' swapi.films

        salt '*' swapi.films 1

    '''

    status, result = _query(action='spaceships',
                            id_key=id_key,
                            method='GET')
    return result


def species(id_key=None, **kwargs):
    '''
    Query Star Wars species

    CLI Example:

    .. code-block:: bash

        salt '*' swapi.films

        salt '*' swapi.films 1

    '''

    status, result = _query(action='species',
                            id_key=id_key,
                            method='GET')
    return result
