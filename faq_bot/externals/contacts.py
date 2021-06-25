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
get a account external key.
"""

__all__ = ['get_account_info']

import tornado.gen
from faq_bot.common.utils import auth_get
from faq_bot.constant import API_BO, OPEN_API
import logging
import json


@tornado.gen.coroutine
def get_account_info(account_id):
    """
    Get account information.

        reference
            - `Common Message Property <https://developers.worksmobile.com/kr/document/1006004/v1?lang=en>`_

    :param account_id: user account id.
    :return: name(user name), department(user department).
    """

    contacts_url = API_BO["contacts_url"]
    contacts_url = contacts_url.replace("_USER_ACCOUNT_ID_", account_id)

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "charset": "UTF-8",
        "consumerKey": OPEN_API["consumerKey"]
    }

    response = auth_get(contacts_url, headers=headers)
    if response.status_code != 200 or response.content is None:
        logging.error("get account info failed. url:%s text:%s body:%s",
                    contacts_url, response.text, response.content)
        raise Exception("get account info. http return code error.")
    tmp_req = json.loads(response.content)
    name = tmp_req.get("name", None)
    department = tmp_req.get("groupName", None)
    return name, department
