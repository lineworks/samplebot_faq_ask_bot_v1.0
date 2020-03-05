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
Start using robots
"""

__all__ = ['register_rich_menun', 'start_content', 'start']

import tornado.web
import tornado.gen
import logging
from faq_bot.model.i18n_data import make_i18n_text
from faq_bot.externals.send_message import push_messages
from faq_bot.common.global_data import get_value
from faq_bot.externals.richmenu import set_user_specific_rich_menu
import gettext
_ = gettext.gettext


@tornado.gen.coroutine
def register_rich_menun(account_id):
    """
    Set up rich menu for chat with users.
    Check also: faq_bot/model/data.py

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1005040?lang=en>`_

    :param account_id: user account id
    """
    if account_id is None:
        logging.error("account_id is None.")
        return False
    rich_menu_id = get_value("rich_menu", None)
    if rich_menu_id is None:
        logging.error("get rich_menu_id failed.")
        raise Exception("get rich_menu_id failed.")

    return set_user_specific_rich_menu(rich_menu_id, account_id)


@tornado.gen.coroutine
def start_content(account_id):
    yield register_rich_menun(account_id)

    fmt = _("Hello. I’m FAQ Ask Bot. "
            "I’m here to answer your office-related questions.")
    content1 = make_i18n_text("Hello. I’m FAQ Ask Bot. "
                              "I’m here to answer your office-related questions.",
                              "start", fmt)

    fmt1 = _("Please select an item from the menu below.")
    content2 = make_i18n_text("Please select an item from the menu below.",
                              "start", fmt1)

    return [content1, content2]


@tornado.gen.coroutine
def start(account_id, _, __):
    """
    Handle the user start using robots.
    Send the robot's self introduction information,
    and the chat room is bound with rich menu.

    :param account_id: user account id.
    """
    contents = yield start_content(account_id)

    yield push_messages(account_id, contents)
