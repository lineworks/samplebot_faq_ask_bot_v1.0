# !/bin/bash python3
# -*- coding: UTF-8 -*-

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
the global setting for faq_bot
"""

from faq_bot.constant import ABSDIR_OF_PARENT

LOG_PATH = ABSDIR_OF_PARENT + "/logs/"
CALENDAR_LOG_FILE = LOG_PATH + "faq_bot.log"
CALENDAR_LOG_ROTATE = "midnight"
CALENDAR_LOG_FMT = '[%(asctime)-15s] [%(levelname)s] ' \
                   '%(filename)s %(funcName)s:%(lineno)d ' \
                   '%(process)d %(request_id).8s %(message)s'
CALENDAR_LOG_LEVEL = "DEBUG"

CALENDAR_PORT = 8080
CALENDAR_PID_FILE = LOG_PATH + "faq_bot.pid"
