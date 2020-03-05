#!/bin/env python3
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
The context for logging request_id
"""
import threading
from logging import Filter
from uuid import uuid4
from tornado.stack_context import StackContext


class RequestContextData(object):
    """
    request_id
    """
    def __init__(self, request_id=0):
        self.request_id = request_id

    def __eq__(self, other):
        return self.request_id == other.request_id


class Metaclass(type):
    """
    meta class for RequestContext
    """
    @property
    def data(cls):
        """
        data property of RequestContext
        """
        if not hasattr(cls._state, 'data'):
            return RequestContextData()
        return cls._state.data


class RequestContext(object, metaclass=Metaclass):
    """
    The context class for request_id
    """
    _state = threading.local()
    _state.data = RequestContextData()

    def __init__(self, request_id=0):
        self._data = RequestContextData(request_id=request_id)

    def __enter__(self):
        self._prev_data = self.__class__._state.data
        self.__class__._state.data = self._data

    def __exit__(self, exc_type, exc_value, traceback):
        self.__class__._state.data = self._prev_data
        del self._prev_data
        return False


class RequestContextFilter(Filter):
    """
    logging filter for add request_id to record
    """
    def filter(self, record):
        """
        add request_id to record
        """
        request_id = RequestContext.data.request_id

        if not request_id:
            request_id = str(threading.current_thread().ident)[::-1]

        record.request_id = request_id

        return True


def contextualizedLogging(handler):
    """
    This class decorator is contextualizing the HTTP request in logging.
    """

    def wrapExecute(_execute):
        """
        the function to return wraper function
        """
        def wrapper(self, transforms, *args, **kwargs):
            """
            the wraper function
            """
            request_id = uuid4().hex
            with StackContext(lambda: RequestContext(request_id)):
                return _execute(self, transforms, *args, **kwargs)

        return wrapper

    handler._execute = wrapExecute(handler._execute)
    return handler
