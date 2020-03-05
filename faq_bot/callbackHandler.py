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
Process requests of users
"""

__all__ = ['CallbackHandler', 'post']

import json
import logging
import tornado.gen
import tornado.web
from faq_bot.check_and_handle_actions import CheckAndHandleActions


class CallbackHandler(tornado.web.RequestHandler):
    """
    Process business requests of users.

    tornado.web.RequestHandler base class for HTTP request handlers.

        reference
        - `Common Message Property <https://www.tornadoweb.org/en/stable/web.html>`_
    """

    @tornado.gen.coroutine
    def post(self):
        """
        Implement the handle to corresponding HTTP method.
        Check also: faq_bot/router.py
        """

        logging.info("request para path:%s", self.request.uri)
        try:
            body = json.loads(self.request.body)
        except json.JSONDecodeError:
            logging.exception('Failed parse json:%s' % self.request.body)
            raise tornado.web.HTTPError(403, "boy is not json.")

        logging.info("request para body:%s", self.request.body)
        checker = CheckAndHandleActions()
        yield checker.execute(body)

        self.finish()
