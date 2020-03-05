#!/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright 2020-present Works Mobile Corp.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""
HTTP method providing authentication
"""

__all__ = ['auth_post', 'auth_get', 'auth_del', 'auth_del']

import requests
import logging
from tornado.web import HTTPError
from faq_bot.common.token import generate_token
from faq_bot.common.global_data import get_value, set_value


def refresh_token():
    my_token = generate_token()
    set_value("token", my_token)
    return my_token


def get_token():
    return get_value("token", None)


def replace_url_bot_no(url):
    bot_no = get_value("bot_no", None)
    if bot_no is None:
        logging.info("internal error. bot no is None")
        raise HTTPError(500, "internal error. bot no is None")

    url = url.replace("_BOT_NO_", bot_no)
    return url


def auth_post(url, data=None,  headers=None, files=None,
              params=None, json=None, refresh_token_flag=False):
    """
    Encapsulates the post method of adding token to headers.
    Check also: faq_bot/common/token.py
    parameters and return values, refer to:

        reference
        - `Common Message Property <https://3.python-requests.org/user/advanced/#request-and-response-objects>`_
    """

    if headers is not None and not refresh_token_flag:
        my_token = get_token()
        if my_token is None:
            my_token = refresh_token()

        headers["Authorization"] = "Bearer " + my_token
        response = requests.post(url, data=data, headers=headers,
                                 files=files, params=params, json=json)

        if response.status_code == 401 or response.status_code == 403:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
            response = requests.post(url, data=data, headers=headers,
                                     files=files, params=params, json=json)
        return response
    else:
        if refresh_token_flag and headers is not None:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
        return requests.post(url, data=data, headers=headers,
                             files=files, params=params, json=json)

    return None


def auth_get(url, headers=None, refresh_token_flag=False):
    """
    Encapsulates the get method of adding token to headers.
    Check also: faq_bot/common/token.py
    parameters and return values, refer to:

        reference
        - `Common Message Property <https://3.python-requests.org/user/advanced/#request-and-response-objects>`_
    """

    if headers is not None and not refresh_token_flag:
        my_token = get_token()
        if my_token is None:
            my_token = refresh_token()

        headers["Authorization"] = "Bearer " + my_token
        response = requests.get(url, headers=headers)

        if response.status_code == 401 or response.status_code == 403:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
            response = requests.get(url, headers=headers)
        return response
    else:
        if refresh_token_flag and headers is not None:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
        return requests.get(url, headers=headers)

    return None


def auth_del(url, headers=None, refresh_token_flag=False):
    """
    Encapsulates the delete method of adding token to headers.
    Check also: faq_bot/common/token.py
    parameters and return values, refer to:

        reference
        - `Common Message Property <https://3.python-requests.org/user/advanced/#request-and-response-objects>`_
    """

    if headers is not None and not refresh_token_flag:
        my_token = get_token()
        if my_token is None:
            my_token = init_token()

        headers["Authorization"] = "Bearer " + my_token
        response = requests.delete(url, headers=headers)

        if response.status_code == 401 or response.status_code == 403:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
            response = requests.delete(url, headers=headers)
        return response
    else:
        if refresh_token_flag and headers is not None:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
        return requests.delete(url, headers=headers)

    return None


def auth_put(url, data=None,  headers=None, files=None,
              params=None, json=None, refresh_token_flag=False):
    """
    Encapsulates the put method of adding token to headers.
    Check also: faq_bot/common/token.py
    parameters and return values, refer to:

        reference
        - `Common Message Property <https://3.python-requests.org/user/advanced/#request-and-response-objects>`_
    """
    if headers is not None and not refresh_token_flag:
        my_token = get_token()
        if my_token is None:
            my_token = refresh_token()

        headers["Authorization"] = "Bearer " + my_token
        response = requests.put(url, data=data, headers=headers,
                                 files=files, params=params, json=json)

        if response.status_code == 401 or response.status_code == 403:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
            response = requests.put(url, data=data, headers=headers,
                                     files=files, params=params, json=json)
        return response
    else:
        if refresh_token_flag and headers is not None:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
        return requests.put(url, data=data, headers=headers,
                             files=files, params=params, json=json)

    return None
