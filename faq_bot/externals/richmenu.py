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
rich menu's api
"""

__all__ = ['upload_content', 'make_add_rich_menu_body', 'set_rich_menu_image',
           'set_user_specific_rich_menu', 'get_rich_menus',
           'cancel_user_specific_rich_menu', 'init_rich_menu']

import io
import logging
import json
import tornado.gen
from faq_bot.model.data import make_size, make_bound, \
     make_add_rich_menu, make_area
from faq_bot.model.i18n_data import make_i18n_postback_action
from faq_bot.common import utils
from faq_bot.constant import API_BO, OPEN_API
from conf.resource import RICH_MENUS
from faq_bot.common.utils import auth_get, auth_post, auth_del
from faq_bot.common.global_data import get_value, set_value
import gettext
_ = gettext.gettext


def upload_content(file_path):
    """
    Upload rich menu background picture.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1005025?lang=en>`_

    :param file_path: resource local path
    :return: resource id
    """
    headers = {
        "consumerKey": OPEN_API["consumerKey"],
        "x-works-apiid": OPEN_API["apiId"]
    }

    files = {'resourceName': open(file_path, 'rb')}

    url = API_BO["upload_url"]
    url = utils.replace_url_bot_no(url)

    logging.info("upload content. url:%s", url)

    response = auth_post(url, files=files, headers=headers)
    if response.status_code != 200:
        logging.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("upload content. http return error.")

    resource_id = response.headers.get("x-works-resource-id", None)
    if resource_id is None:
        logging.error("invalid content. url:%s txt:%s headers:%s", url,
                      response.text, response.headers)
        raise Exception("upload content. not fond 'x-works-resource-id'.")
    return resource_id


def make_add_rich_menu_body(rich_menu_name):
    """
    add rich menu body

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100504001?lang=en>`_

    :param rich_menu_name: rich menu name
    :return: rich menu id
    """
    size = make_size(2500, 1686)

    fmt1 = _("\"Find FAQ\" by task")

    bound1 = make_bound(0, 0, 2500, 1160)
    action1 = make_i18n_postback_action("query", "richmenu",
                                        "\"Find FAQ\" by task", fmt1,
                                        "\"Find FAQ\" by task",
                                        fmt1)

    fmt2 = _("Send a question")
    bound2 = make_bound(0, 1160, 1250, 526)
    action2 = make_i18n_postback_action("enquire", "richmenu",
                                        "Send a question", fmt2,
                                        "Send a question", fmt2)

    fmt3 = _("Go to Initial Menu")
    bound3 = make_bound(1250, 1160, 1250, 526)
    action3 = make_i18n_postback_action("to_first", "richmenu",
                                        "Go to Initial Menu", fmt3,
                                        "Go to Initial Menu", fmt3)

    rich_menu = make_add_rich_menu(
                    rich_menu_name,
                    size,
                    [
                        make_area(bound1, action1),
                        make_area(bound2, action2),
                        make_area(bound3, action3)
                    ])

    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]

    url = API_BO["rich_menu_url"]
    url = utils.replace_url_bot_no(url)

    logging.info("register richmenu. url:%s", url)

    response = auth_post(url, data=json.dumps(rich_menu), headers=headers)
    if response.status_code != 200:
        logging.info("register richmenu failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("register richmenu. http return error.")

    tmp = json.loads(response.content)
    rich_menu_id = tmp.get("richMenuId", None)
    if rich_menu_id is None:
        logging.error("register richmenu failed. url:%s txt:%s body:%s",
                     url, response.text, response.content)
        raise Exception("register richmenu failed. rich menu id is None.")

    logging.info("register richmenu success. url:%s txt:%s body:%s",
                 url, response.text, response.content)

    return rich_menu_id


def set_rich_menu_image(resource_id, rich_menu_id):
    """
    Set a rich menu image.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100504002?lang=en>`_

    :param resource_id: resource id
    :param rich_menu_id: rich menu id
    :return:
    """
    body = {"resourceId": resource_id}

    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]

    url = API_BO["rich_menu_url"] + "/" + rich_menu_id + "/content"
    url = utils.replace_url_bot_no(url)

    response = auth_post(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        logging.info("set rich menu image failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("set richmenu image. http return error.")

    logging.info("set rich menu image success. url:%s txt:%s body:%s",
                url, response.text, response.content)


def set_user_specific_rich_menu(rich_menu_id, account_id):
    """
    Set a user-specific rich menu.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100504010?lang=en>`_

    :param rich_menu_id: rich menu id
    :param account_id: user account id
    """
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    url = API_BO["rich_menu_url"] + "/" \
          + rich_menu_id + "/account/" + account_id

    url = utils.replace_url_bot_no(url)

    response = auth_post(url, headers=headers)
    if response.status_code != 200:
        logging.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("set user specific richmenu. http return error.")
    logging.info("set user specific richmenu success. url:%s txt:%s body:%s",
                url, response.text, response.content)


def get_rich_menus(name=None):
    """
    Get rich menus

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100504004?lang=en>`_

    :return: rich menu list
    """
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    url = API_BO["rich_menu_url"]
    url = utils.replace_url_bot_no(url)

    logging.info("push message begin. url:%s", url)
    response = auth_get(url, headers=headers)
    if response.status_code != 200:
        logging.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        return None

    logging.info("push message success. url:%s txt:%s body:%s",
                url, response.text, response.content)

    tmp = json.loads(response.content)
    menus = tmp.get("richmenus", None)

    if menus is None:
        return None

    menu_ids = {}
    for menu in menus:
        if menu is not None:
            menu_name = menu.get("name", None)
            menu_id = menu.get("richMenuId", None)
            if menu_name is not None and menu_id is not None:
                if name is not None and menu_name == name:
                    return menu_id
                menu_ids[menu_name] = menu_id
        return menu_ids
    return None


def cancel_user_specific_rich_menu(account_id):
    """
    Cancel a user-specific rich menu

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100504012?lang=en>`_

    :param account_id: user account id
    """
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    url = API_BO["rich_menu_url"] + "/account/" + account_id
    url = utils.replace_url_bot_no(url)

    response = auth_del(url, headers=headers)
    if response.status_code != 200:
        logging.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("canncel user specific richmenu. http return error.")
    logging.info("push message success. url:%s txt:%s body:%s",
                url, response.text, response.content)


def init_rich_menu(local):
    """
    init rich menu.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1005040?lang=en>`_

    :return: rich menu id
    """
    rich_menu_id = get_rich_menus(RICH_MENUS[local]["name"])
    if rich_menu_id is None:
        rich_menu_id = make_add_rich_menu_body(RICH_MENUS[local]["name"])
        resource_id = upload_content(RICH_MENUS[local]["path"])
        set_rich_menu_image(resource_id, rich_menu_id)

    set_value("rich_menu", rich_menu_id)

