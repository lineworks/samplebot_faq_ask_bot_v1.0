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
Handle user selection ask a person
"""

__all__ = ['enquire']

import tornado.web
import tornado.gen
from faq_bot.model.i18n_data import make_i18n_text
from faq_bot.actions.message import create_quick_replay
from faq_bot.externals.send_message import push_message
from faq_bot.model.cachehandle import set_replace_user_info
import gettext
_ = gettext.gettext

@tornado.gen.coroutine
def enquire(account_id, __, ___):
    """
    This function handles the user's selection of ask a person

    :param account_id: user account id.
    """
    set_replace_user_info(account_id, "none", "doing", "none")
    fmt = _("Select a task related to your question.")
    content = make_i18n_text("Select a task related to your question.",
                             "enquire", fmt)

    content["quickReply"] = create_quick_replay()

    yield push_message(account_id, content)
