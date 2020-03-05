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
Functions dealing with articles.
"""

__all__ = ['create_boards', 'get_boards', 'create_articles', 'init_board']

import tornado.gen
import logging
import json
import tornado.gen
from tornado.web import HTTPError
from requests.exceptions import ConnectionError
from requests_toolbelt import MultipartEncoder
from faq_bot.common.utils import auth_get, auth_post
from faq_bot.constant import API_BO, OPEN_API
from conf.resource import BOARDS
from conf.config import DOMAIN_ID
from faq_bot.actions.message import create_articles_failed, storage_lack
from faq_bot.externals.contacts import get_account_info
from faq_bot.common.global_data import get_value, set_value


def create_boards(board):
    """
    Create boards.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100180201?lang=en>`_
    :return: board no
    """
    body = {
        "domainId": DOMAIN_ID,
        "title": board["title"],
        "description": board["description"],
        "boardType": "BOARD"
    }

    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]

    boards_url = API_BO["home"]["boards_url"]
    response = auth_post(boards_url, data=json.dumps(body), headers=headers)

    if response.status_code != 200 or response.content is None:
        logging.error("create boards failed. url:%s text:%s headers:%s body:%s",
                    boards_url, response.text, json.dumps(headers), json.dumps(body))
        raise Exception("create boards. http return code error.")
    tmp_req = json.loads(response.content)
    board_no = tmp_req.get("boardNo", None)
    if board_no is None:
        raise Exception("create boards. board no filed is None.")
    return board_no


def get_boards(title=None):
    """
    Create boards.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100180202?lang=en>`_

    :return: If boards have been created, the information of boards no will be returned;
            otherwise, none will be returned.
    """

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "charset": "UTF-8",
        "consumerKey": OPEN_API["consumerKey"]
    }

    boards_url = "%s?domainId=%d" % (API_BO["home"]["boards_url"], DOMAIN_ID)
    response = auth_get(boards_url, headers=headers)

    if response.status_code != 200 or response.content is None:
        logging.error("get boards failed. url:%s text:%s headers:%s ",
                    boards_url, response.text, json.dumps(headers))
        raise Exception("get boards. http return code error.")

    tmp_req = json.loads(response.content)
    boards = tmp_req.get("boards", None)
    if boards is None:
        return None

    board_nos = {}
    for board in boards:
        if board is not None:
            bord_title = board.get("title", None)
            bord_no = board.get("boardNo", None)
            if bord_title is not None and bord_no is not None:
                if title is not None and bord_title == title:
                    return bord_no
                board_nos[bord_title] =  bord_no
    if title is not None:
        return None
    return board_nos


@tornado.gen.coroutine
def create_articles(title, type, content, account_id=None,
                    attention_period_in_days=None):
    """
    Create articles.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100180301?lang=en>`_
    """

    headers = {
        "charset": "UTF-8",
        "consumerKey": OPEN_API["consumerKey"]
    }

    board_no = get_value("{type}board".format(type=type), None)
    if board_no is None:
        logging.error("create articles. board no is None.")
        raise HTTPError(500, "create articles. board no is None.")

    body = {
        "title": title,
        "body": content,
        "boardNo": board_no,
        "domainId": DOMAIN_ID,
        "sendCreatedNotify": True,
        "useComment": True
    }

    if account_id is not None:
        body["accountId"] = account_id

    if attention_period_in_days is not None:
        body["attentionPeriodInDays"] = attention_period_in_days

    multi1 = MultipartEncoder(
        fields={"article":(None, json.dumps(body))}
    )

    headers['content-type'] = multi1.content_type
    boards_url = API_BO["home"]["create_articles_url"]

    try:
        response = auth_post(boards_url, data=multi1, headers=headers)
    except ConnectionError as ex:
        logging.exception("create articles failed. url:%s headers:%s "
                          "body:%s error:%s",
                          boards_url, json.dumps(headers),
                          json.dumps(body), ex)
        return create_articles_failed()

    if response.status_code != 200 or response.content is None:
        logging.error(
            "create articles failed. url:%s text:%s headers:%s body:%s",
            boards_url, response.text, json.dumps(headers), json.dumps(body))

        if response.status_code == 507:
            return storage_lack()
        else:
            return create_articles_failed()

    tmp_req = json.loads(response.content)
    article_no = tmp_req.get("articleNo", None)
    if article_no is None:
        logging.error("create articles failed. url:%s text:%s",
                     boards_url, response.text)
        raise HTTPError(500, "create articles. article no is None.")
    return None


def init_board(local):
    """
    Initialize board. Check also: faq_bot/externals/richmenu.py
    please check home API.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1001801?lang=en>`_
    """

    boards = get_boards()
    for type in BOARDS:
        board = BOARDS[type][local]
        if board["title"] in boards:
            set_value("{type}board".format(type=type),
                      boards[board["title"]])
        else:
            board_no = create_boards(board)
            set_value("{type}board".format(type=type), board_no)



