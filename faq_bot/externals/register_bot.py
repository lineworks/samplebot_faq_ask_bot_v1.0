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
Initialize bot no.
"""

__all__ = ['get_message_bot_from_remote', 'register_bot',
           'register_bot_domain', 'init_bot']

import json
import requests
import logging
from faq_bot.model.i18n_data import get_i18n_content
from faq_bot.constant import PRIVATE_KEY_PATH, DEVELOP_API_DOMAIN, \
    API_BO, CALLBACK_ADDRESS, PHOTO_URL, BOT_NAME
from conf.config import API_ID, DOMAIN_ID, ADMIN_ACCOUNT, LOCAL_ADDRESS, \
    SERVER_CONSUMER_KEY
from faq_bot.common.utils import auth_post, auth_get
from faq_bot.common.global_data import get_value, set_value
import gettext
_ = gettext.gettext

def headers():
    my_headers = {
        "consumerKey": SERVER_CONSUMER_KEY,
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }
    return my_headers


def get_message_bot_from_remote():
    """
    get a message bot.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1005006?lang=en>`_

    :return: bot no
    """
    url = API_BO["bot"]
    response = auth_get(url, headers=headers())
    if response.status_code != 200:
        logging.info("register bot domain field: code:%d content:%s" % (
            response.status_code, response.text))
        return None

    content = json.loads(response.content)
    bots = content.get("bots", None)
    if bots is None:
        return None
    for bot in bots:
        name = bot.get("name", None)
        photo_url = bot.get("photoUrl", None)
        if name == BOT_NAME and photo_url == PHOTO_URL:
            return bot.get("botNo", None)
    return None


def register_bot():
    """
    Register a message bot.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1005002?lang=en>`_

    :param photo_address: Access address of user's Avatar,
        If you need to change the user image,
        please replace the corresponding file in the image/, Only PNG file.
    :return: bot no
    """
    url = API_BO["bot"]
    fmt = _("FAQ Ask Bot")
    a = lambda x, y: {"language": x, "name": y}
    b = lambda x, y: {"language": x, "description": y}
    data = {
        "name": BOT_NAME,
        "i18nNames": get_i18n_content(fmt, "register_bot", function=a),
        "photoUrl": PHOTO_URL,
        "description": BOT_NAME,
        "i18nDescriptions": get_i18n_content(fmt, "register_bot", function=b),
        "managers": [ADMIN_ACCOUNT],
        "submanagers": [],
        "useGroupJoin": False,
        "useDomainScope": False,
        "useCallback": True,
        "callbackUrl": CALLBACK_ADDRESS,
        "callbackEvents": ["text", "location", "sticker", "image"]
    }

    response = auth_post(url, data=json.dumps(data), headers=headers())
    if response.status_code != 200:
        raise Exception("register bot field: code:%d text:%s" % (response.status_code, response.text))

    tmp = json.loads(response.content)
    bot_no = tmp.get('botNo', None)
    if bot_no is None:
        raise Exception("register bot field: bot no is None")
    return bot_no


def register_bot_domain(bot_no):
    """
    Register a message bot domain.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1005004?lang=en>`_

    :param bot_no: bot no
    """
    url = API_BO["bot"] +"/"+ str(bot_no) + "/domain/" + str(DOMAIN_ID)
    data = {"usePublic": True, "usePermission": False}
    response = auth_post(url, data=json.dumps(data), headers=headers())
    if response.status_code != 200:
        raise Exception("register bot domain field: code:%d content:%s" % (
        response.status_code, response.text))


def init_bot():
    """
    Initialize bot info. If the BOT is not registered, the system will fail to start.

    Before BOT registration,
    If BOT has been registered, it does not need to be re registered.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/2005001?lang=en>`_

    """
    bot_no = get_message_bot_from_remote()
    if bot_no is None:
        bot_no = register_bot()
        register_bot_domain(bot_no)

    # todo set cache
    set_value("bot_no", str(bot_no))
