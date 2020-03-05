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
Handle "find FAQ" by task
"""

__all__ = ['template_introduce']

import tornado.gen
from conf.resource import CAROUSEL
from faq_bot.model.data import make_list_template
from faq_bot.model.i18n_data import make_i18n_text, make_i18n_message_action, \
    make_i18n_list_template_element
from faq_bot.model.cachehandle import set_replace_user_info

from faq_bot.externals.send_message import push_messages
import gettext
_ = gettext.gettext


def template_introduce():
    """
    This function constructs three image carousels for self introduction.
    Check also: faq_bot/model/data.py

        reference
        - `Common Message Property <https://developers.worksmobile.com/kr/document/100500805?lang=en>`_

    :return: image carousels type message content.
    """
    fmt = _("See FAQs")
    action0 = make_i18n_message_action("query_leave", "query", "See FAQs", fmt,
                                       "See FAQs", fmt)
    action1 = make_i18n_message_action("query_welfare", "query", "See FAQs",
                                       fmt, "See FAQs", fmt)
    action2 = make_i18n_message_action("query_security", "query", "See FAQs",
                                       fmt, "See FAQs", fmt)

    fmt_title0 = _("HR/Leave")
    fmt_subtitle0 = _("See FAQs about HR and leave.")
    element0 = make_i18n_list_template_element("query", "HR/Leave",
                                               "See FAQs about HR and leave.",
                                               image=CAROUSEL["leave"][0],
                                               action=action0,
                                               fmt_title=fmt_title0,
                                               fmt_subtitle=fmt_subtitle0)
    fmt_title1 = _("Welfare/Work support")
    fmt_subtitle1 = _("See FAQs about welfare and work support.")
    element1 = make_i18n_list_template_element("query", "Welfare/Work support",
                                               "See FAQs about welfare "
                                               "and work support.",
                                               image=CAROUSEL["welfare"][0],
                                               action=action1,
                                               fmt_title=fmt_title1,
                                               fmt_subtitle=fmt_subtitle1)
    fmt_title2 = _("Security")
    fmt_subtitle2 = _("See FAQs about security.")
    element2 = make_i18n_list_template_element("query", "Security",
                                               "See FAQs about security.",
                                               image=CAROUSEL["security"][0],
                                               action=action2,
                                               fmt_title = fmt_title2,
                                               fmt_subtitle = fmt_subtitle2)

    return make_list_template([element0, element1, element2])

@tornado.gen.coroutine
def query(account_id, __, ___):
    """
    This Function to deal "find FAQ" by task.
    :param account_id: user account id.
    """
    set_replace_user_info(account_id, "none", "doing", "none")
    fmt = _("Please select an work-related item that you would like to know.")
    content1 = make_i18n_text("Please select an work-related item "
                         "that you would like to know.", "query", fmt)

    content2 = template_introduce()

    yield push_messages(account_id, [content1, content2])