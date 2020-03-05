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
Handle user's transfer from query business to ask a person
"""

__all__ = ['transfer_message']

import tornado.web
import tornado.gen
import asyncio
from tornado.web import HTTPError
from faq_bot.model.i18n_data import make_i18n_text
from faq_bot.constant import TYPES
from faq_bot.externals.send_message import push_messages
from faq_bot.model.cachehandle import set_replace_user_info, \
    get_user_status, set_user_status
import gettext
_ = gettext.gettext


@tornado.gen.coroutine
def transfer_message(account_id, callback, __):
    """
    This function prompts the user to go to ask someone.

    :param account_id: user account id.
    :param callback: Business type.
    """
    status, __, ___, ____ = get_user_status(account_id)
    if status is not None:
        set_user_status(account_id, status="none")

    fmt = _("Your question will be directly delivered to the person "
            "in charge of {type} to answer your question directly.")
    content1 = make_i18n_text("Your question will be directly delivered to "
                         "the person in charge of {type} "
                         "to answer your question directly.".format(
        type=TYPES[callback]), "transfer_message", fmt, type=callback)

    fmt1 = _("Please tell me your question.\n\nOnly one message can be delivered. "
             "Please write your question at one go.")
    content2 = make_i18n_text("Please tell me your question.\n\n"
                              "Only one message can be delivered. "
                              "Please write your question at one go.",
                              "transfer_message", fmt1)

    yield  asyncio.sleep(0.5)
    set_replace_user_info(account_id, 'wait_in', 'doing', callback)

    yield push_messages(account_id, [content1, content2])