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
This is a global variable cache.
"""

__all__ = ['set_value', 'get_value']

_global_dict = {}


def _init():
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    """
    Sets a value into the global variable cache.
    :param key: key
    :param value: value
    :return: no
    """
    _global_dict[key] = value


def get_value(key, def_value=None):
    """
    Gets a value from the global variable cache.
    :param key: key
    :param def_value: default value
    :return: value, If the key does not exist, the default value.
    """
    try:
        return _global_dict[key]
    except KeyError:
        return def_value
