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
send message to user
"""

__all__ = ['push_message', 'push_messages']

import io
import logging
import json
import tornado.gen
from tornado.web import HTTPError
from faq_bot.common.utils import auth_post, replace_url_bot_no
from faq_bot.constant import API_BO, OPEN_API


@tornado.gen.coroutine
def push_message(account_id, content, header=None):
    """
    Send message to user. the package is the following JSON structure.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1005008?lang=en>`_

    :param account_id: user account id
    :param content: message content
    :param header: http header
    """

    if content is None:
        logging.info("content is None.")
        raise HTTPError(500, "internal error. content is None.")

    request = {
        "accountId": account_id,
        "content": content
    }

    headers = API_BO["headers"]
    if header is not None:
        headers = Merge(header, headers)

    headers["consumerKey"] = OPEN_API["consumerKey"]

    url = API_BO["push_url"]
    url = replace_url_bot_no(url)
    response = auth_post(url, data=json.dumps(request), headers=headers)
    if response.status_code != 200:
        logging.error("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise HTTPError(500, "internal error. Internal interface call error.")


@tornado.gen.coroutine
def push_messages(account_id, contents):
    """
    Send multiple messages to users

    :param account_id: user account id
    :param contents: message content list
    """
    if contents is None:
        logging.info("contents is None.")
        raise HTTPError(500, "internal error. contents is None.")

    for content in contents:
        yield push_message(account_id, content)
