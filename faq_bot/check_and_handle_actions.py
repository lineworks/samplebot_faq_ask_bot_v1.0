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
Factory used to create handler and execute handler.
"""

__all__ = ['CheckAndHandleActions', 'execute']

import time
import logging
import tornado.gen
from datetime import datetime
from tornado.web import HTTPError
from faq_bot.actions.to_first import to_first
from faq_bot.actions.enquire import enquire
from faq_bot.actions.query import query
from faq_bot.actions.start import start
from faq_bot.actions.cancel import cancel
from faq_bot.actions.modify import modify
from faq_bot.actions.send import send
from faq_bot.actions.query_leave import query_leave
from faq_bot.actions.query_security import query_security
from faq_bot.actions.query_welfare import query_welfare
from faq_bot.actions.deal_message import deal_message
from faq_bot.actions.transfer_message import transfer_message
from faq_bot.actions.enquire_message import enquire_message


class CheckAndHandleActions:
    """
    Factory used to create handler and execute handler.
    """

    __text = ""
    __post_back = ""
    __account_id = None
    __content_type = ""
    __content_post_back = ""
    __type = "none"
    __handle = None
    __user_message = None

    def __init__(self):
        pass

    @tornado.gen.coroutine
    def execute(self, body):
        """
        Verify the body parameter and execute handler.
        Please refer to the reference link of the function.

            reference
            - `Common Message Property <https://developers.worksmobile.com/jp/document/100500901?lang=en>`_
        """

        handle_map = {
            'start': start,
            'query': query,
            'to_first': to_first,
            'enquire': enquire,
            'enquire_': enquire_message,
            'query_leave': query_leave,
            'query_welfare': query_welfare,
            'query_security': query_security,
            'transfer_': transfer_message,
            'send': send,
            'modify': modify,
            'cancel': cancel
        }

        if body is None or "source" not in body or "accountId" \
                not in body["source"]:
            raise HTTPError(403, "can't find 'accountId' field.")
        if "type" not in body:
            raise HTTPError(403, "can't find 'type' field.")

        self.__account_id = body["source"].get("accountId", None)

        if self.__account_id is None:
            raise HTTPError(403, "'accountId' is None.")

        type = body.get("type", "")
        
        content = body.get("content", None)
        if content is not None:
            self.__content_type = content.get("type", "")
            self.__content_post_back = content.get("postback", "")
            self.__text = content.get("text", None)

        if type == "postback":
            self.__post_back = body.get("data", "")

        if type == "message" and self.__content_type == "text" \
                and self.__content_post_back == "":
            self.__user_message = self.__text
            self.__handle = deal_message

        else:
            if self.__post_back.find("enquire_") != -1:
                pos = self.__post_back.find("enquire_")
                self.__type = self.__post_back[pos + 8:]
                self.__post_back = "enquire_"

            elif self.__post_back.find("transfer_") != -1:
                pos = self.__post_back.find("transfer_")
                self.__type = self.__post_back[pos + 9:]
                self.__post_back = "transfer_"

            if self.__post_back in handle_map:
                self.__handle = handle_map[self.__post_back]
            elif self.__content_post_back in handle_map:
                self.__handle = handle_map[self.__content_post_back]

        if self.__handle is not None:
            yield self.__handle(self.__account_id, self.__type,
                                self.__user_message)
        else:
            raise HTTPError(400, "Error 'callback' type.")
        return
