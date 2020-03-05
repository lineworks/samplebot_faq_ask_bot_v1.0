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
Process user confirmation message content
"""
import tornado.web
import tornado.gen
from conf.config import DEFAULT_LANG
from faq_bot.model.i18n_data import make_i18n_text, get_i18n_content_by_lang
from faq_bot.constant import TYPES
from faq_bot.externals.contacts import get_account_info
from faq_bot.actions.message import create_quick_replay
from faq_bot.externals.send_message import push_messages
from faq_bot.externals.home import create_articles
from faq_bot.model.cachehandle import get_user_status, clean_user_status
import gettext
_ = gettext.gettext


@tornado.gen.coroutine
def send(account_id, __, ___):
    """
    This function processes the content of the user confirmation message

    :param account_id: user account.
    """
    status, __, type, message = get_user_status(account_id)
    if status != "done" or message is None:
        # todo add error prompt
        raise HTTPError(500, "user status error. status error")

    fmt = _("Your question has been sent to the person in charge. \n\n"
            "The staff will answer your question as soon as possible.")
    content = make_i18n_text(
        "Your question has been sent to the person in charge. \n\n"
        "The staff will answer your question as soon as possible.",
        "send", fmt)

    fmt = _("If you have any additional questions, "
            "please select the task from below. "
            "If you want to go back to the initial stage, "
            "select [Go to Initial Menu] from the menu below.")
    content1 = make_i18n_text("If you have any additional questions, "
                              "please select the task from below. "
                              "If you want to go back to the initial stage, "
                              "select [Go to Initial Menu] from the menu below.",
                              "send", fmt)

    content1["quickReply"] = create_quick_replay()
    name, department = yield get_account_info(account_id)
    fmt = _("{department} {name} made an inquiry.")
    title = get_i18n_content_by_lang(fmt, "send", DEFAULT_LANG,
                                     department=department, name=name)
    prompt_message = yield create_articles(title, type, message, account_id)
    if prompt_message is not None:
        yield push_messages(account_id, [prompt_message])
        return

    clean_user_status(account_id)
    yield push_messages(account_id, [content, content1])