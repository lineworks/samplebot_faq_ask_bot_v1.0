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
Generate token according to JWT protocol
"""

__all__ = ['create_tmp_token', 'generate_token']

import python_jwt as jwt
import jwcrypto.jwk as jwk
import datetime
import requests
import json
from faq_bot.constant import API_BO, HEROKU_SERVER_ID, \
    PRIVATE_KEY_PATH


def create_tmp_token(key_path, server_id):
    """
    This function use JWT protocol to creates a temporary token
    for user authentication.

    Focus on the "Server Token (ID Registration Style)" section of
    the following documents.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1002002?lang=en>`_
    """

    with open(key_path, "rb") as _file:
        key = _file.read()
        private_key = jwk.JWK.from_pem(key)
        payload = {"iss": server_id}
        token = jwt.generate_jwt(payload, private_key, 'RS256',
                                 datetime.timedelta(minutes=5))
        return token
    return None


def generate_token():
    """
    Using JWT protocol to create token.
    Focus on the "Server Token (ID Registration Style)" section of
    the following documents.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1002002?lang=en>`_
    """

    tmp_token = create_tmp_token(PRIVATE_KEY_PATH, HEROKU_SERVER_ID)
    if tmp_token is None:
        raise Exception("generate tmp token failed.")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "charset": "UTF-8"
    }
    url = API_BO["auth_url"] + tmp_token
    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        raise Exception("generate token failed.")

    content = json.loads(response.content)
    token = content.get("access_token", None)
    if token is None:
        raise Exception("response token is None.")

    return token
