# -*- coding: utf-8 -*-

"""
requests.api
~~~~~~~~~~~~

This module provides shared variables and the core Inkah classes.

:copyright: (c) 2016 by Mike Leonard.
:license: MIT, see LICENSE for more details.
"""

__version__ = '0.0.1'


from .utils import generate_id
from abc import ABCMeta, abstractmethod

import json
import socket
import time


TRACE_ID_HEADER = 'X-Inkah-Trace-ID'
PARENT_SPAN_ID_HEADER = 'X-Inkah-Parent-Span-ID'
REQUEST_ID_HEADER = 'X-Inkah-Request-ID'

SPAN_BEGIN  = 'SPANBEGIN'
SPAN_END  = 'SPANEND'
SPAN_ANNOTATE  = 'SPANNOTATE'
REQUEST_BEGIN  = 'REQUESTBEGIN'
REQUEST_END  = 'REQUESTEND'


class AbstractInkahSpan:
    __metaclass__ = ABCMeta

    _publish_socket = None
    _app = None
    _app_name = None
    _daemon_host = None
    _daemon_port = None

    @abstractmethod
    def begin(self): raise NotImplementedError()

    @abstractmethod
    def end(self): raise NotImplementedError()

    # @abstractmethod
    # def publish_request_start(self, request_id): raise NotImplementedError()

    # @abstractmethod
    # def publish_request_end(self, request_id): raise NotImplementedError()

    @abstractmethod
    def annotate(self, message): raise NotImplementedError()

    @classmethod
    def init(cls, app):
        cls._app = app
        cls._app_name = app.name
        cls._daemon_host = app.config['INKAH_DAEMON_HOST']
        cls._daemon_port = app.config['INKAH_DAEMON_PORT']
        # Set up the socket now ready for use as requests come in.
        if cls._publish_socket is None:
            cls._publish_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class InkahDummySpan(AbstractInkahSpan):
    def begin(self): pass
    def end(self): pass
    # def publish_request_start(self, request_id): pass
    # def publish_request_end(self, request_id): pass
    def annotate(self, message): pass


class InkahSpan(AbstractInkahSpan):
    def __init__(self, trace_id=None, parent_span_id=None):
        self.trace_id = trace_id
        self.parent_id = parent_span_id
        self.id = generate_id()

    def serialize_event(self, timestamp, event_type, data=None):
        message_data = ''
        if data is not None:
            # Convert dict {'a': 1, 'b': 2} to a set ('a', 1, 'b', 2), convert
            # each value to a string and then join with ':'
            message_data = ':'.join(['' if x is None else str(x) for x in sum(data.items(), ())])

        # Use modulo operator here for formatting strings as its known to
        # be most performant for join string.
        event = '%s:%s:%s:%s:%s:%s:%s' % (timestamp, self._app.name,
                                          self.trace_id, self.id,
                                          self.parent_id, event_type,
                                          message_data
                                         )

        return event

    def _publish(self, event_type, data=None):
        timestamp = int(time.time())
        message = self.serialize_event(timestamp, event_type, data)
        self._publish_socket.sendto(message, (self._daemon_host, self._daemon_port))

    def begin(self):
        self._publish(SPAN_BEGIN)

    def end(self):
        self._publish(SPAN_END)

    def annotate(self, message):
        self._publish(SPAN_ANNOTATE, {'message': message})
