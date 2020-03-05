#!/bin/env python
# -*- coding: utf-8 -*-
"""
Initialize bot no.
"""

__all__ = ['create_bot', 'add_domain', 'init_bot']
import sys
import json
import requests
sys.path.append('./')
from faq_bot.constant import PRIVATE_KEY_PATH, DEVELOP_API_DOMAIN, \
    API_BO, PHOTO_URL, BOT_NAME
from conf.resource import BOARDS
from conf.config import API_ID, DOMAIN_ID, ADMIN_ACCOUNT, LOCAL_ADDRESS, \
    SERVER_CONSUMER_KEY
from faq_bot.common.token import generate_token


def headers():
    token = generate_token()
    my_headers = {
        "consumerKey": SERVER_CONSUMER_KEY,
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }
    return my_headers


def deletes(ids, function):
    if ids is None:
        return
    for id in ids:
        function(id)


def delete_bot(bot_no):
    """
    Deletes a message bot.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1005011?lang=en>`_

    :return: bot no
    """
    url = API_BO["bot"] + "/" + str(bot_no)
    response = requests.delete(url, headers=headers())
    if response.status_code != 200:
        print("delete bot domain field: code:%d content:%s bot_no:%d" % (
        response.status_code, response.text, bot_no))

def get_message_bots():
    """
    get a message bot.
        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1005006?lang=en>`_
    :return: bot no
    """
    url = API_BO["bot"]
    response = requests.get(url, headers=headers())
    if response.status_code != 200:
        print("register bot domain field: code:%d content:%s" % (
            response.status_code, response.text))
        return None

    content = json.loads(response.content)
    bots = content.get("bots", None)
    if bots is None:
        return None

    del_bots = []
    for bot in bots:
        name = bot.get("name", None)
        photo_url = bot.get("photoUrl", None)
        if name == BOT_NAME and photo_url == PHOTO_URL:
            bot_no = bot.get("botNo", None)
            del_bots.append(bot_no)
    return del_bots

def delete_board(board_nos):
    boards_url = "%s/remove" % (API_BO["home"]["boards_url"],)
    data = {
        "domainId": DOMAIN_ID,
        "removeBoardNos": board_nos
    }

    response = requests.post(boards_url, data=json.dumps(data),
                             headers=headers())

    if response.status_code != 200:
        print("delete boards failed. url:%s code:%d text:%s headers:%s board_nos:%s"%(boards_url, response.status_code,
              response.text, headers(), str(board_nos)))

def get_boards(titles=None):
    """
    Create boards.
        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100180202?lang=en>`_

    :return: If boards have been created, the information of boards no will be returned;
            otherwise, none will be returned.
    """

    boards_url = "%s?domainId=%d" % (API_BO["home"]["boards_url"], DOMAIN_ID)
    response = requests.get(boards_url, headers=headers())
    if response.status_code != 200 or response.content is None:
        print("get boards failed. code:%d url:%s text:%s",
              response.status_code, boards_url, response.text)
        return None

    tmp_req = json.loads(response.content)
    boards = tmp_req.get("boards", None)
    if boards is None:
        return None

    board_nos = []
    for board in boards:
        if board is not None:
            bord_title = board.get("title", None)
            bord_no = board.get("boardNo", None)
            if bord_title is not None and bord_no is not None:
                if titles is not None and bord_title in titles:
                    board_nos.append(bord_no)
    return board_nos


if __name__ == "__main__":
    bots = get_message_bots()
    deletes(bots, delete_bot)

    titles = []
    for lang_values in BOARDS.values():
        for value in lang_values.values():
            titles.append(value['title'])
    boards = get_boards(titles)
    delete_board(boards)




