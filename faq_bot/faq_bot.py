#!/bin/bash python
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
launch faq_bot
"""

__all__ = ['sig_handler', 'kill_server', 'init_logger',
           'start_faq_bot']

import os
import logging
from logging import StreamHandler
import asyncio
import uvloop
import json
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.httpclient import AsyncHTTPClient
from tornado.options import define, options
from faq_bot.externals.richmenu import init_rich_menu
from faq_bot.externals.home import init_board
from faq_bot.common import global_data
from faq_bot.constant import API_BO
from conf.config import DEFAULT_LANG
from faq_bot.externals.register_bot import init_bot

import psutil
import faq_bot.router
import faq_bot.contextlog
from faq_bot.settings import CALENDAR_PORT, CALENDAR_LOG_FMT, \
    CALENDAR_LOG_LEVEL, CALENDAR_LOG_FILE, CALENDAR_LOG_ROTATE

define("port", default=CALENDAR_PORT, help="server listen port. "
                                           "default 8080")
define("workers", default=0, help="the count of workers. "
                                  "default the same as cpu cores")
define("logfile", default=None, help="the path for log")

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def sig_handler(sig, _):
    """
    signal handler
    """
    print("sig %s received" % str(sig))
    try:
        parent = psutil.Process(os.getpid())
        children = parent.children()
        for process in children:
            process.send_signal(sig)
    except (psutil.NoSuchProcess, psutil.ZombieProcess,
            psutil.AccessDenied) as ex:
        print(str(ex))
    tornado.ioloop.IOLoop.instance().add_callback(kill_server)


def kill_server():
    """
    stop the ioloop
    """
    asyncio.get_event_loop().stop()


def init_logger():
    """
    Initializes the root logger settings.
    """
    formatter = logging.Formatter(CALENDAR_LOG_FMT)
    root_logger = logging.getLogger()
    file_handler = StreamHandler()
    file_handler.setFormatter(formatter)

    root_logger.setLevel(CALENDAR_LOG_LEVEL)
    file_handler.addFilter(faq_bot.contextlog.RequestContextFilter())
    root_logger.addHandler(file_handler)

    logging.getLogger("tornado.application").addHandler(file_handler)
    logging.getLogger("tornado.general").addHandler(file_handler)


def start_faq_bot():
    """
    the faq_bot launch code

    tornado.httpserver a non-blocking, single-threaded HTTP server.

        reference
        - `Common Message Property <https://www.tornadoweb.org/en/stable/httpserver.html>`_

    tornado.routing flexible routing implementation.

        reference
        - `Common Message Property <https://www.tornadoweb.org/en/stable/routing.html>`_

    If you use the event loop that comes with tornado, many third-party
    packages based on asyncio may not be used, such as aioredis.

    Message bot API overview.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/3005001?lang=en>`_
    """

    server = tornado.httpserver.HTTPServer(faq_bot.router.getRouter())

    server.bind(options.port)
    server.start(1)

    init_logger()
    init_bot()
    init_rich_menu(DEFAULT_LANG)
    init_board(DEFAULT_LANG)

    asyncio.get_event_loop().run_forever()
    server.stop()
    asyncio.get_event_loop().close()

    print("exit...")
