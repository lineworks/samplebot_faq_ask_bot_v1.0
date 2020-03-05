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
create message content
"""

__all__ = ['make_postback_action', 'make_message_action', 'make_url_action',
           'make_normal_action', 'make_quick_reply_item', 'make_quick_reply',
           'make_text', 'make_add_rich_menu', 'make_carousel_column',
           'make_carousel', 'make_list_template_element', 'make_list_template',
           'make_i18n_content_texts', 'i18n_text', 'make_i18n_label',
           'i18n_display_text', 'make_i18n_image_url', 'make_i18n_subtitle',
           'make_i18n_thumbnail_image_url', 'make_i18n_title']

import json

def make_i18n_label(language, label):
    return {"language": language, "label": label}


def i18n_display_text(language, display_text):
    return {"language": language, "displayText": display_text}


def make_postback_action(data, label=None, i18n_labels=None,
                         display_text=None, i18n_display_texts=None):
    """
    make post back action.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1005050?lang=en>`_

    :param data: post back string
    :return: actions content
    """

    action = {"type": "postback", "data": data}

    if display_text is not None:
        action["displayText"] = display_text
    if label is not None:
        action["label"] = label
    if i18n_labels is not None:
        action["i18nLabels"] = i18n_labels
    if i18n_display_texts is not None:
        action["i18nDisplayTexts"] = i18n_display_texts

    return action


def i18n_text(language, text):
    return {"language": language, "text": text}


def make_message_action(post_back, label, i18n_labels=None,
                        text=None, i18n_texts=None):
    """
    make message action.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1005050?lang=en>`_

    :param post_back: post back string
    :return: actions content
    """

    action = {"type": "message", "label": label, "postback": post_back}
    if text is not None:
        action["text"] = text
    if i18n_labels is not None:
        action["i18nLabels"] = i18n_labels
    if i18n_texts is not None:
        action["i18nTexts"] = i18n_texts

    return action


def make_url_action(label, url, i18n_labels=None):
    """
    make url action.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1005050?lang=en>`_

    :param url: User behavior will trigger the client to request this URL.
    :return: actions content
    """

    if i18n_labels is not None:
        return {"type": "uri", "label": label, "uri": url,
                "i18nLabels": i18n_labels}
    return {"type": "uri", "label": label, "uri": url}


def make_normal_action(atype, label, i18n_labels=None):
    """
    Create camera, camera roll, location action.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1005050?lang=en>`_

    :param atype: action's type
    :return: None
    """
    if i18n_labels is not None:
        return {"type": atype, "label": label, "i18nLabels": i18n_labels}
    return {"type": atype, "label": label}


def make_i18n_thumbnail_image_url(language, thumbnail_image_url):
    return {"language": language, "thumbnailImageUrl": thumbnail_image_url}


def make_i18n_image_resource_id(language, image_resource_id):
    return {"language": language, "imageResourceId": image_resource_id}


def make_quick_reply_item(action,
                          url=None,
                          image_resource_id=None,
                          i18n_thumbnail_image_urls=None,
                          i18n_image_resource_ids=None):
    """
    Create quick reply message item.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100500807?lang=en>`_

    :param action: The user clicks the quick reply button to trigger this action.
    :return: quick reply content.
    """

    reply_item = {"action": action}
    if url is not None:
        reply_item["imageUrl"] = url
    if image_resource_id is not None:
        reply_item["imageResourceId"] = image_resource_id
    if i18n_thumbnail_image_urls is not None:
        reply_item["i18nImageUrl"] = i18n_thumbnail_image_urls
    if i18n_image_resource_ids is not None:
        reply_item["i18nImageResourceIds"] = i18n_image_resource_ids
    return reply_item


def make_quick_reply(replay_items):
    """
    Create quick reply message.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100500807?lang=en>`_

    :param replay_items: Array of return object of make_quick_reply_item function.
    :return: quick reply content.
    """
    return {"items": replay_items}


def make_text(text, i18n_texts=None):
    """
    make text.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100500801?lang=en>`_

    :return: text content.
    """
    if i18n_texts is not None:
        return {"type": "text", "text": text, "i18nTexts": i18n_texts}
    return {"type": "text", "text": text}


def make_i18n_image_url(language, image_url):
    return {"language": language, "imageUrl": image_url}


def make_size(w, h):
    return {"width": w, "height": h}


def make_bound(x, y, w, h):
    return {"x": x, "y": y, "width": w, "height": h}


def make_area(bound, action):
    return {"bounds": bound, "action": action}


def make_add_rich_menu(name, size, areas):
    """
    add rich menu content:

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/1005040?lang=en>`_

    You can create a rich menu for the message bot by following these steps:
    1. Image uploads: using the "Upload Content" API
    2. Rich menu generation: using the "Register Message Rich Menu" API
    3. Rich Menu Image Settings: Use the "Message Rich Menu Image Settings" API
    """

    return {"name": name, "size": size, "areas": areas}


def make_i18n_content_texts(language, content_text):
    return {"language": language, "contentText": content_text}


def make_i18n_thumbnail_resource_id(language, resource_id):
    return {"language": language, "thumbnailImageResourceId": resource_id}


# make_i18n_thumbnail_image_url
def make_carousel_column(text, actions, title=None, image_url=None,
                         resource_id=None, default_action=None,
                         i18n_image_urls=None, i18_resource_ids=None,
                         i18n_texts=None, i18n_titles=None):
    """
    create carousel message column content.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100500808?lang=en>`_
    """

    content = {"text": text, "actions": actions}
    if title is not None:
        content["title"] = title
    if image_url is not None:
        content["thumbnailImageUrl"] = image_url
    if resource_id is not None:
        content["thumbnailImageResourceId"] = resource_id
    if default_action is not None:
        content["defaultAction"] = default_action
    if i18n_texts is not None:
        content["i18nTexts"] = i18n_texts
    if i18n_titles is not None:
        content["i18nTitles"] = i18n_titles
    if i18n_image_urls is not None:
        content["i18nThumbnailImageUrls"] = i18n_image_urls
    if i18_resource_ids is not None:
        content["i18nThumbnailImageResourceIds"] = i18_resource_ids
    return content


def make_carousel(columns, ratio=None, size=None):
    """
    create carousel message content.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100500808?lang=en>`_
    """

    content = {"type": "carousel", "columns": columns}
    if ratio is not None:
        content["imageAspectRatio"] = ratio
    if size is not None:
        content["imageSize"] = size
    return content



def make_i18n_title(language, title):
    return {"language": language, "title": title}


def make_i18n_subtitle(language, subtitle):
    return {"language": language, "subtitle": subtitle}


def make_i18n_image(language, image):
    return {"language": language, "image": image}


def make_i18n_resource_id(language, resource_id):
    return {"language": language, "resourceId": resource_id}


def make_list_template_element(title, subtitle=None, image=None,
                               resource_id=None, action=None, i18n_titles=None,
                               i18n_subtitles=None, i18n_images=None,
                               i18n_resource_ids=None):
    """
    create carousel list template a Row.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100500805?lang=en>`_
    """
    content = {
        "title": title
    }

    if subtitle is not None:
        content["subtitle"] = subtitle

    if image is not None:
        content["image"] = image

    if resource_id is not None:
        content["resourceId"] = resource_id

    if action is not None:
        content["action"] = action

    if i18n_titles is not None:
        content["i18nTitles"] = i18n_titles

    if i18n_subtitles is not None:
        content["i18nSubtitles"] = i18n_subtitles

    if i18n_images is not None:
        content["i18nImages"] = i18n_images

    if i18n_resource_ids is not None:
        content["resourceIds"] = i18n_resource_ids

    return content


def make_i18n_background_image(language, image):
    return {"language": language, "backgroundImage": image}


def make_i18n_background_resource_id(language, resource_id):
    return {"language": language, "backgroundResourceId": resource_id}


def make_cover_data(title=None, subtitle=None, background_image=None,
                    background_resource_id=None, i18n_titles=None,
                    i18n_subtitles=None, i18n_background_images=None,
                    i18n_background_resource_ids=None):
    content = {}
    if title is not None:
        content["title"] = title

    if subtitle is not None:
        content["subtitle"] = subtitle

    if background_image is not None:
        content["backgroundImage"] = background_image

    if background_resource_id is not None:
        content["backgroundResourceId"] = background_resource_id

    if i18n_titles is not None:
        content["i18nTitles"] = i18n_titles

    if i18n_subtitles is not None:
        content["i18nSubtitles"] = i18n_subtitles

    if i18n_background_images is not None:
        content["i18nBackgroundImages"] = i18n_background_images

    if i18n_background_resource_ids is not None:
        content["i18nBackgroundImages"] = i18n_background_resource_ids

    return content


def make_list_template(elements, cover_data=None, actions=None):
    """
    create carousel list template.

        reference
        - `Common Message Property <https://developers.worksmobile.com/jp/document/100500805?lang=en>`_
    """
    content = {"type": "list_template", "elements": elements}

    if cover_data is not None:
        content["coverData"] = cover_data

    if actions is not None:
        content["actions"] = actions

    return content






