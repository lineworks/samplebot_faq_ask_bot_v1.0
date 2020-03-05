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
Deal with issues related to leave query
"""

__all__ = ['query_leave']

import tornado.gen
import tornado.web
import logging
from conf.resource import CAROUSEL, POST_BACK_URLS
from faq_bot.model.i18n_data import make_i18n_text
from faq_bot.actions.message import create_quick_replay_item, create_carousel
from faq_bot.externals.send_message import push_messages
from faq_bot.model.cachehandle import set_user_status, get_user_status
import gettext
_ = gettext.gettext

@tornado.gen.coroutine
def query_leave(account_id, __, ___):
    """
    This function deals with the problems related to leave query.

    :param account_id: user account id.
    """
    status, __, type, message = get_user_status(account_id)
    if status == "wait_in":
        set_user_status(account_id, status="none")

    fmt = _("Here are FAQs about HR and leave.")
    text = make_i18n_text("Here are FAQs about HR and leave.", "query_leave", fmt)

    fmt = _("Send a question")
    replay = create_quick_replay_item("transfer_leave", "query_leave", "Send a question", fmt)

    labels = ["See more", "See more", "See more", "See more"]

    fmt = _("See more")
    i18n_label_fmts = [fmt, fmt, fmt, fmt]

    titles = [
        "The types of leave.",
        "How many days of leave I have?",
        "To request a leave.",
        "To cancel my leave."
    ]

    i18n_title_fmts = [
        _("The types of leave."),
        _("How many days of leave I have?"),
        _("To request a leave."),
        _("To cancel my leave.")
    ]

    texts = [
        "Types of leave are classified in the Labor Standards Act.",
        "The remaining days of your leave are on in-house browser.",
        "You can request a leave via the in-house browser.",
        "You can cancel your leave request via the in-house browser."
    ]

    i18n_text_fmts = [
        _("Types of leave are classified in the Labor Standards Act."),
        _("The remaining days of your leave are on in-house browser."),
        _("You can request a leave via the in-house browser."),
        _("You can cancel your leave request via the in-house browser.")
    ]

    carousel = create_carousel("query_leave", labels, POST_BACK_URLS["leave"],
                               texts, titles, CAROUSEL["leave"],
                               fmt_labels=i18n_label_fmts,
                               fmt_texts=i18n_text_fmts,
                               fmt_titles=i18n_title_fmts)

    carousel["quickReply"] = replay

    yield push_messages(account_id, [text, carousel])

