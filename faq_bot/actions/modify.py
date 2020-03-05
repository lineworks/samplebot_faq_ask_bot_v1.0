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
Deal with users' modification of questions
"""

__all__ = ['modify']

import tornado.web
import tornado.gen
import asyncio
from faq_bot.model.i18n_data import make_i18n_text
from faq_bot.externals.send_message import push_message
from faq_bot.model.cachehandle import set_user_status, get_user_status
import gettext
_ = gettext.gettext

@tornado.gen.coroutine
def modify(account_id, __, ___):
    """
    This function handles the user's modification of the question

    :param account_id: user account id.
    """
    status, __, ___, ____ = get_user_status(account_id)
    if status != "done":
        raise HTTPError(500, "user status error. status error")

    fmt = _("I’ll help you modify your question. "
            "Please write your question again.")
    content = make_i18n_text("I’ll help you modify your question. Please write"
                             " your question again.", "modify", fmt)

    yield asyncio.sleep(0.5)

    set_user_status(account_id, status='wait_in')

    yield push_message(account_id, content)