# !/bin/env python
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
deal user input messages
"""

__all__ = ['deal_message']

import tornado.web
import tornado.gen
import asyncio
from tornado.web import HTTPError
from faq_bot.model.data import make_text
from faq_bot.actions.message import echo_display
from faq_bot.externals.send_message import push_message
from faq_bot.model.cachehandle import set_user_status, get_user_status


@tornado.gen.coroutine
def deal_message(account_id, __, message):
    """
    Process messages manually entered by the user.

    :param account_id: user account id.
    :param message: user input message.
    """
    yield asyncio.sleep(0.2)
    status, _, __, ___  = get_user_status(account_id)
    if status != "wait_in":
        raise HTTPError(403, "Messages not need to be processed")

    content = echo_display(message)
    set_user_status(account_id, status="done", message=message)

    yield push_message(account_id, content)