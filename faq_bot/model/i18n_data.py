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
create i18n message content
"""

__all__ = ['get_i18n_content', 'get_i18n_content_by_lang', 'make_i18n_button',
           'make_i18n_text', 'make_i18n_message_action', 'make_i18n_url_action',
           'make_i18n_postback_action', 'make_i18n_carousel_column',
           'make_i18n_list_template_element']

import json
from faq_bot.model.data import *
import gettext
import locale
_ = gettext.gettext


def get_i18n_type(type):
    fmt0 = _('HR/Leave')
    fmt1 = _('Welfare/Work support')
    fmt2 = _('Security')

    i18n_type = {
        'leave': fmt0,
        'welfare': fmt1,
        'security': fmt2
    }

    ko = gettext.translation('i18n_data', 'locales', ['ko'])
    en = gettext.translation('i18n_data', 'locales', ['en'])
    ja = gettext.translation('i18n_data', 'locales', ['ja'])

    fmt = i18n_type[type]

    return {'en_US': en.gettext(fmt), 'ja_JP': ja.gettext(fmt),
            'ko_KR': ko.gettext(fmt)}


def get_i18n_content(fmt, local, **kw):
    """
    Get multilingual data structure according to format parameter id.

        reference
        - `Common Message Property <https://docs.python.org/2/library/gettext.html>`_

    :param fmt: Multilingual key string. like _('This is a translatable string.')
    :param local: Domain corresponding to "fmt".
    :param kw: Named variable parameter list.
        Common parameters:
            function: A callback function used to encapsulate multiple languages.
            type: Business type
    :return:
        If the parameter contains the package function of the package, An encapsulated multilingual dictionary object will be returned.
        If the parameter does not contain a package function, this returns a Multilingual list object.
    """
    ko = gettext.translation(local, 'locales', ['ko'])
    en = gettext.translation(local, 'locales', ['en'])
    ja = gettext.translation(local, 'locales', ['ja'])

    i18n_content = {}
    function = None
    if 'function' in kw:
        function = kw['function']
        if function is not None:
            i18n_content = []

    type = None
    i18n_types = None
    if 'type' in kw:
        type = kw['type']
        i18n_types = get_i18n_type(type)
        del kw['type']

    for lang in [('en_US', en), ('ja_JP', ja), ('ko_KR', ko)]:

        if function is not None:
            if len(kw) > 0:
                if type is not None:
                    i18n_content_item = function(lang[0],
                                                 lang[1].gettext(fmt).format(
                                                     type=i18n_types[lang[0]],
                                                     **kw))
                else:
                    i18n_content_item = function(lang[0],
                                                 lang[1].gettext(fmt).format(
                                                     **kw))
            else:
                if type is not None:
                    i18n_content_item = function(lang[0],
                                                 lang[1].gettext(fmt).format(
                                                     type=i18n_types[lang[0]]))
                else:
                    i18n_content_item = function(lang[0],
                                                 lang[1].gettext(fmt))

            i18n_content.append(i18n_content_item)
        elif len(kw) > 0:
            if type is not None:
                i18n_content[lang[0]] = lang[1].gettext(fmt).format(
                    type=i18n_types[lang[0]], **kw)
            else:
                i18n_content[lang[0]] = lang[1].gettext(fmt).format(**kw)
        else:
            if type is not None:
                i18n_content[lang[0]] = lang[1].gettext(fmt).format(
                    type=i18n_types[lang[0]])
            else:
                i18n_content[lang[0]] = lang[1].gettext(fmt)
    return i18n_content


def get_i18n_content_by_lang(fmt, local, lang, **kw):
    """
    Get another language string according to key string.

        reference
        - `Common Message Property <https://docs.python.org/2/library/gettext.html>`_

    :param fmt: Multilingual key string. like _('This is a translatable string.')
    :param local: Domain corresponding to "fmt".
    :param lang: Language. ['en'|'ko'|'ja']
    :param kw: Named variable parameter list.
    :return: a string.
    """
    local_text = gettext.translation(local, 'locales', [lang])

    if len(kw) > 0:
        content = local_text.gettext(fmt).format(**kw)
    else:
        content = local_text.gettext(fmt)
    return content


def make_i18n_button(text, actions, local, fmt):
    """
    Create a multilingual button object.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100500804?lang=en>`_

        Check also: faq_bot/model/data.py::make_button
    """
    i18n_texts = get_i18n_content(fmt, local, function=make_i18n_content_texts)
    return make_button(text, actions, content_texts=i18n_texts)


def make_i18n_text(text, local, fmt, **kw):
    """
    Create a multilingual text object.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100500801?lang=en>`_

        Check also: faq_bot/model/data.py::make_text
    """
    i18n_texts = get_i18n_content(fmt, local, function=i18n_text, **kw)
    return make_text(text, i18n_texts=i18n_texts)


def make_i18n_message_action(post_back, local, label, fmt_label=None,
                             text=None, fmt_text=None):
    """
    Create a multilingual message action object.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1005050?lang=en>`_

        Check also: faq_bot/model/data.py::make_message_action
    """
    i18n_labels = None
    if fmt_label is not None:
        i18n_labels = get_i18n_content(fmt_label, local,
                                       function=make_i18n_label)

    i18n_texts = None
    if fmt_text is not None:
        i18n_texts = get_i18n_content(fmt_text, local, function=i18n_text)
    return make_message_action(post_back, label, i18n_labels=i18n_labels,
                               text=text, i18n_texts=i18n_texts)


def make_i18n_postback_action(post_back, local, label, fmt_label=None,
                              text=None, fmt_text=None):
    """
    Create a multilingual postback action object.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1005050?lang=en>`_

        Check also: faq_bot/model/data.py::make_postback_action
    """
    i18n_labels = None
    if fmt_label is not None:
        i18n_labels = get_i18n_content(fmt_label, local,
                                       function=make_i18n_label)

    i18n_texts = None
    if fmt_text is not None:
        i18n_texts = get_i18n_content(fmt_text, local,
                                      function=i18n_display_text)

    return  make_postback_action(post_back, label, i18n_labels,
                                 text, i18n_texts)

def make_i18n_url_action(local, label, uri, fmt_label=None):
    """
    Create a multilingual uri action object.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1005050?lang=en>`_

        Check also: faq_bot/model/data.py::make_uri_action
    """
    i18n_labels = None
    if fmt_label is not None:
        i18n_labels = get_i18n_content(fmt_label, local,
                                       function=make_i18n_label)

    return make_url_action(label, uri, i18n_labels=i18n_labels)


def  make_i18n_carousel_column(locale, text, actions, title=None, image_url=None,
                              default_action=None, fmt_text=None,
                              fmt_title=None, fmt_url=None):
    """
    Create a multilingual carousel column object.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100500808?lang=en>`_

        Check also: faq_bot/model/data.py::make_carousel_column
    """
    i18n_image_urls = None
    if fmt_url is not None:
        i18n_image_urls = get_i18n_content(fmt_label, locale,
                                           function=make_i18n_thumbnail_image_url)

    i18n_texts = None
    if fmt_text is not None:
        i18n_texts = get_i18n_content(fmt_text, locale,
                                      function=i18n_text)

    i18n_titles = None
    if fmt_title is not None:
        i18n_titles = get_i18n_content(fmt_title, locale,
                                       function=make_i18n_title)

    return make_carousel_column(text, actions, title=title, image_url=image_url,
                                default_action=default_action,
                                i18n_image_urls=i18n_image_urls,
                                i18n_texts=i18n_texts,
                                i18n_titles=i18n_titles)


def make_i18n_list_template_element(locale, title, subtitle=None, image=None,
                               resource_id=None, action=None, fmt_title=None,
                               fmt_subtitle=None, fmt_image=None,
                               fmt_resource=None):
    """
    Create a list template element object.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100500805?lang=en>`_

        Check also: faq_bot/model/data.py::make_list_template_element
    """
    i18n_titles = None
    if fmt_title is not None:
        i18n_titles = get_i18n_content(fmt_title, locale,
                                       function=make_i18n_title)
    i18n_subtitles = None
    if fmt_subtitle is not None:
        i18n_subtitles = get_i18n_content(fmt_subtitle, locale,
                                          function=make_i18n_subtitle)
    i18n_images = None
    if fmt_image is not None:
        i18n_images = get_i18n_content(fmt_image, locale,
                                       function=make_i18n_image)
    i18n_resource_ids = None
    if fmt_resource is not None:
        i18n_resource_ids = get_i18n_content(fmt_resource, locale,
                                             function=make_i18n_resource_id)

    return make_list_template_element(title, subtitle=subtitle, image=image,
                                      resource_id=resource_id, action=action,
                                      i18n_titles=i18n_titles,
                                      i18n_subtitles=i18n_subtitles,
                                      i18n_images=i18n_images,
                                      i18n_resource_ids=i18n_resource_ids)
