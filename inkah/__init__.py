# -*- coding: utf-8 -*-

"""
requests.api
~~~~~~~~~~~~

This module provides shared variables and the core Inkah classes.

:copyright: (c) 2016 by Mike Leonard.
:license: MIT, see LICENSE for more details.
"""

__version__ = '0.0.1'

import socket
import uuid

TRACE_ID_HEADER = 'X-Inkah-Trace-ID'
PARENT_SPAN_ID_HEADER = 'X-Inkah-Parent-Span-ID'


def generate_id():
    return str(uuid.uuid1())


class InkahSpan(object):
    _publish_socket = None
    program_name = None

    def __init__(self, trace_id=None, span_id=None, parent_span_id=None):
        if InkahSpan.program_name is None:
            # This shouldn't throw and exception but just log it and ideally
            # get it in to Inkah.
            # Maybe ERROR:program_name:message?
            raise Exception('program_name is not set.')
        self.trace_id = trace_id
        self.id = span_id
        self.parent_id = parent_span_id

    @staticmethod
    def init_publish_socket():
        if InkahSpan._publish_socket is None:
            InkahSpan._publish_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def publish(self, message_type, message=None):
        if self.id:
            message = '{program}:{trace_id}:{span_id}:{parent_id}:{type}:{message}'.format(
                program=self.program_name, trace_id=self.trace_id,
                span_id=self.id, parent_id=self.parent_id,
                type=message_type, message=message
                )

            InkahSpan._publish_socket.sendto(message, ('127.0.0.1', 9800))

    def publish_begin(self):
        if self.id:
            self.publish('SPANBEGIN')

    def publish_end(self):
        if self.id:
            self.publish('SPANEND')

    def annotate(self, message):
        if self.id:
            self.publish('SPANANNOTATE', message)
