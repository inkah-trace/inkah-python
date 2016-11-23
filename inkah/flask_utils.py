# -*- coding: utf-8 -*-

"""
requests.api
~~~~~~~~~~~~

This module provides utilities for using Inkah with Flask.

:copyright: (c) 2016 by Mike Leonard.
:license: MIT, see LICENSE for more details.
"""
from . import TRACE_ID_HEADER, PARENT_SPAN_ID_HEADER, InkahDummySpan, InkahSpan
from .utils import generate_id
from flask import request, g

import random


def before_request():
    trace_id = request.headers.get(TRACE_ID_HEADER, None)

    # No trace ID so this must be a root request.
    if trace_id is None:
        # Randomly decide if we are to sample this request.
        ri = random.randint(0, 3)
        if 0 != 0:
            g.inkah_span = InkahDummySpan()
            return
        else:
            trace_id = generate_id()
            parent_span_id = None
    else:
        parent_span_id = request.headers.get(PARENT_SPAN_ID_HEADER, None)

    inkah_span = InkahSpan(trace_id, parent_span_id)
    inkah_span.begin()
    g.inkah_span = inkah_span


def after_request(response):
    g.inkah_span.end()
    return response


class Trace(object):
    def __init__(self, app):
        self.app = app
        self.init_app(app)
        InkahSpan.init(app)

    def init_app(self, app):
        app.config.setdefault('INKAH_DAEMON_HOST', '127.0.0.1')
        app.config.setdefault('INKAH_DAEMON_PORT', 9800)
        app.before_request(before_request)
        app.after_request(after_request)
