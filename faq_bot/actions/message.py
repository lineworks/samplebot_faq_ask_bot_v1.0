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
common message
"""

__all__ = ['create_quick_replay_item', 'create_carousel',
           'create_quick_replay', 'echo_display']

from faq_bot.model.data import make_quick_reply_item, \
    make_carousel_column, make_carousel, make_quick_reply
from faq_bot.model.i18n_data import make_i18n_text, make_i18n_postback_action, \
    make_i18n_url_action, make_i18n_carousel_column
import gettext
_ = gettext.gettext

def invalid_message():
    fmt = _("I’m sorry. I couldn't understand the words. \n\n"
            "Please select the function you want "
            "from Bot Menu at the bottom of the chat window.")

    return make_i18n_text("I’m sorry. I couldn't understand the words. \n\n"
                          "Please select the function you want from Bot Menu "
                          "at the bottom of the chat window.", "message", fmt)

def create_articles_failed():
    fmt = _("Failed to complete posting. \n\n"
            "Ask the FAQ Ask Bot manager to check if the bulletin board number "
            "does not exist or if other items are set up incorrectly.")
    return make_i18n_text("Failed to complete posting. \n\n"
                          "Ask the FAQ Ask Bot manager to check if the bulletin"
                          " board number does not exist or if other items are "
                          "set up incorrectly.", "message", fmt)

def storage_lack():
    fmt = _("Failed to complete posting. \n\n"
            "Ask the in-house manager if the public capacity is not enough or "
            "if the capacity available for domain use has been exceeded.")
    return make_i18n_text("Failed to complete posting. \n\n"
                          "Ask the in-house manager if the public capacity is "
                          "not enough or if the capacity available for "
                          "domain use has been exceeded.", "message", fmt)

def create_quick_replay():
    """
    Building a quick reply floating window for messages.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100500807?lang=en>`_

    Check also: faq_bot/model/data.py
    :return: quick replay item
    """
    fmt0 = _("HR/Leave")
    action0 = make_i18n_postback_action("enquire_leave", "message", "HR/Leave",
                                        fmt0, "HR/Leave", fmt0)
    item0 = make_quick_reply_item(action0)

    fmt1 = _("Welfare/Work support")
    action1 = make_i18n_postback_action("enquire_welfare", "message",
                                   "Welfare/Work support", fmt1,
                                   "Welfare/Work support", fmt1)
    item1 = make_quick_reply_item(action1)

    fmt2 = _("Security")
    action2 = make_i18n_postback_action("enquire_security", "message", "Security",
                                   fmt2, "Security", fmt2)
    item2 = make_quick_reply_item(action2)

    return make_quick_reply([item0, item1, item2])


def echo_display(message):
    """
    Generate messages that require user confirmation.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100500807?lang=en>`_

    Check also: faq_bot/model/data.py
    :param message: User input message.
    :return: Message to prompt users.
    """
    text = "Do you want to send the following as your question? \n\n" \
           "===\n{message}\n===".format(message=message)
    fmt = _("Do you want to send the following as your question? \n\n===\n{message}\n===")
    content = make_i18n_text(text, "message", fmt, message=message)

    fmt0 = _("Send")
    action0 = make_i18n_postback_action("send", "message", "Send", fmt0,
                                        "Send", fmt0)
    item0 = make_quick_reply_item(action0)

    fmt1 = _("Modify")
    action1 = make_i18n_postback_action("modify", "message", "Modify", fmt1,
                                        "Modify", fmt1)
    item1 = make_quick_reply_item(action1)

    fmt2 = _("Cancel")
    action2 = make_i18n_postback_action("cancel", "message", "Cancel", fmt2,
                                        "Cancel", fmt2)
    item2 = make_quick_reply_item(action2)

    quick_reply = make_quick_reply([item0, item1, item2])

    content["quickReply"] = quick_reply

    return content

def create_quick_replay_item(callback, locale, label, fmt_label=None, text=None,
                             fmt_text=None):
    """
    Building a quick reply floating window for messages.
    Check also: faq_bot/model/data.py

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100500807?lang=en>`_

    :param callback: callback string for the button.
    :return: quick replay item
    """

    if text is None:
        text = label
        if fmt_text is None and fmt_label is not None:
            fmt_text = fmt_label

    action = make_i18n_postback_action(callback, locale, label, fmt_label,
                                       text, fmt_text)

    item = make_quick_reply_item(action)
    return make_quick_reply([item])

def create_carousel(locale, labels, urls, texts, titles, image_urls,
                    fmt_labels=None, fmt_texts=None, fmt_titles=None):
    """
    Building a quick reply floating window for messages.
    Check also: faq_bot/model/data.py

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100500807?lang=en>`_

    :return: return carousel content
    """
    action0 = make_i18n_url_action(locale, labels[0], urls[0], fmt_labels[0])
    column0 = make_i18n_carousel_column(locale, texts[0], [action0],
                                        title=titles[0],
                                        image_url=image_urls[0],
                                        default_action=action0,
                                        fmt_text=fmt_texts[0],
                                        fmt_title=fmt_titles[0])

    action1 = make_i18n_url_action(locale, labels[1], urls[1], fmt_labels[1])
    column1 = make_i18n_carousel_column(locale, texts[1], [action1],
                                        title=titles[1],
                                        image_url=image_urls[1],
                                        default_action=action1,
                                        fmt_text=fmt_texts[1],
                                        fmt_title=fmt_titles[1])

    action2 = make_i18n_url_action(locale, labels[2], urls[2], fmt_labels[2])
    column2 = make_i18n_carousel_column(locale, texts[2], [action2],
                                        title=titles[2],
                                        image_url=image_urls[2],
                                        default_action=action2,
                                        fmt_text=fmt_texts[2],
                                        fmt_title=fmt_titles[2])

    action3 = make_i18n_url_action(locale, labels[3], urls[3], fmt_labels[3])
    column3 = make_i18n_carousel_column(locale, texts[3], [action3],
                                        title=titles[3],
                                        image_url=image_urls[3],
                                        default_action=action3,
                                        fmt_text=fmt_texts[3],
                                        fmt_title=fmt_titles[3])

    return make_carousel([column0, column1, column2, column3], ratio="square")