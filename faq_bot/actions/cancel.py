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
Deal cancel ask a person
"""

__all__ = ['cancel']

import tornado.web
import tornado.gen
from faq_bot.model.i18n_data import make_i18n_text
from faq_bot.externals.send_message import push_message
from faq_bot.model.cachehandle import get_user_status, clean_user_status
import gettext
_ = gettext.gettext

@tornado.gen.coroutine
def cancel(account_id, __, ___):
    """
    This function handles user cancellation inquiry.

    :param account_id: user account id.
    """
    status, ____, __, ___ = get_user_status(account_id)
    if status != "done":
        # todo add error prompt
        raise HTTPError(500, "user status error. status error")

    fmt = _("You have canceled your question. "
            "Please re-select the task from the menu below.")
    content = make_i18n_text("You have canceled your question. "
                             "Please re-select the task from the menu below.",
                             "cancel", fmt)
    clean_user_status(account_id)
    yield push_message(account_id, content)