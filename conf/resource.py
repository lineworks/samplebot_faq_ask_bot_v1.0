#!/bin/bash python3
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
resource.py Defining the resource address used for a project.
"""

from conf.config import LOCAL_ADDRESS
from faq_bot.constant import ABSDIR_OF_PARENT

# RICH_MENUS
RICH_MENUS = {
    'en': {
        "name": "faq_bot_rich_menu_en",
        "path": ABSDIR_OF_PARENT + "/image/en/Rich_Menu.png"
    },
    'ko': {
        "name": "faq_bot_rich_menu_ko",
        "path": ABSDIR_OF_PARENT + "/image/kr/Rich_Menu.png"
    },
    'ja': {
        "name": "faq_bot_rich_menu_ja",
        "path": ABSDIR_OF_PARENT + "/image/jp/Rich_Menu.png"
    }

}

BOARDS = {
    'leave': {
        'en': {
            "title": "HR/Vacation Inquiry",
            "description": "HR/Vacation Inquiry",
        },
        'ja': {
            "title": "人事/休暇のお問い合わせ内容",
            "description": "人事/休暇のお問い合わせ内容",
        },
        'ko': {
            "title": "인사/휴가 문의 내역",
            "description": "인사/휴가 문의 내역",
        }
    },

    'welfare':{
        'en': {
            "title": "Welfare/Business Support Inquiry",
            "description": "Welfare/Business Support Inquiry",
        },
        'ja': {
            "title": "福利厚生/業務支援のお問い合わせ内容",
            "description": "福利厚生/業務支援のお問い合わせ内容",
        },
        'ko': {
            "title": "복지/업무지원 문의 내역",
            "description": "복지/업무지원 문의 내역",
        }
    },

    'security': {
        'en': {
            "title": "Security Inquiry",
            "description": "Security Inquiry",
        },
        'ja': {
            "title": "セキュリティのお問い合わせ内容",
            "description": "セキュリティのお問い合わせ内容",
        },
        'ko': {
            "title": "보안 문의 내역",
            "description": "보안 문의 내역",
        }

    }
}

# API ADDRESS
CAROUSEL = {
    "leave": [
        LOCAL_ADDRESS + "static/carousel/Carousel_01.png",
        LOCAL_ADDRESS + "static/carousel/Carousel_02.png",
        LOCAL_ADDRESS + "static/carousel/Carousel_03.png",
        LOCAL_ADDRESS + "static/carousel/Carousel_04.png"
    ],
    "welfare": [
        LOCAL_ADDRESS + "static/carousel/Carousel_05.png",
        LOCAL_ADDRESS + "static/carousel/Carousel_06.png",
        LOCAL_ADDRESS + "static/carousel/Carousel_07.png",
        LOCAL_ADDRESS + "static/carousel/Carousel_08.png"
    ],
    "security": [
        LOCAL_ADDRESS + "static/carousel/Carousel_09.png",
        LOCAL_ADDRESS + "static/carousel/Carousel_10.png",
        LOCAL_ADDRESS + "static/carousel/Carousel_11.png",
        LOCAL_ADDRESS + "static/carousel/Carousel_12.png"
    ]
}

POST_BACK_URLS = {
    "leave": [
        "https://community.worksmobile.com/jp/",
        "https://community.worksmobile.com/jp/",
        "https://community.worksmobile.com/jp/",
        "https://community.worksmobile.com/jp/"
    ],
    "welfare": [
        "https://community.worksmobile.com/jp/",
        "https://community.worksmobile.com/jp/",
        "https://community.worksmobile.com/jp/",
        "https://community.worksmobile.com/jp/"
    ],
    "security": [
        "https://community.worksmobile.com/jp/",
        "https://community.worksmobile.com/jp/",
        "https://community.worksmobile.com/jp/",
        "https://community.worksmobile.com/jp/"
    ]
}
