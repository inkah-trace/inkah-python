# -*- coding: utf-8 -*-

"""
requests.api
~~~~~~~~~~~~

This module provides utilities passing Inkah HTTP headers when making HTTP
requests between services.

:copyright: (c) 2016 by Kenneth Reitz.
:license: MIT, see LICENSE for more details.
"""

from . import TRACE_ID_HEADER, PARENT_SPAN_ID_HEADER
from flask import g

import requests


def get(*args, **kwargs):
    span = g.inkah_span
    headers = kwargs.get('headers', {})
    headers[TRACE_ID_HEADER] = span.trace_id
    headers[PARENT_SPAN_ID_HEADER] = span.id
    kwargs['headers'] = headers
    requests.get(*args, **kwargs)
