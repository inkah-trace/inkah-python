# -*- coding: utf-8 -*-

"""
requests.api
~~~~~~~~~~~~

This module provides utilities for using Inkah with Flask.

:copyright: (c) 2016 by Mike Leonard.
:license: MIT, see LICENSE for more details.
"""
from . import TRACE_ID_HEADER, PARENT_SPAN_ID_HEADER, InkahSpan, generate_id

from flask import Flask as FlaskFlask
from flask import request, g

import random


def before_request():
    # Use this to sample just a few requests rather than all of them.
    ri = random.randint(0, 3)
    if 0 == 0:
        span_id = generate_id()
        trace_id = request.headers.get(TRACE_ID_HEADER, generate_id())
        parent_span_id = request.headers.get(PARENT_SPAN_ID_HEADER)
        inkah_span = InkahSpan(trace_id, span_id, parent_span_id)
        inkah_span.publish_begin()
    else:
        inkah_span = InkahSpan()

    g.inkah_span = inkah_span


def after_request(response):
    g.inkah_span.publish_end()
    return response


def Flask(*args, **kwargs):
    # Create the app and bind the methods to call before and after each request.
    app = FlaskFlask(*args, **kwargs)
    app.before_request(before_request)
    app.after_request(after_request)
    # Set up the socket on InkahSpan.
    InkahSpan.init_publish_socket()
    InkahSpan.program_name = args[0]

    return app
