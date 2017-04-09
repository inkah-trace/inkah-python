from __future__ import absolute_import

import wrapt

from flask import request, g

from inkah import Span, TRACE_ID_HEADER, SPAN_ID_HEADER, PARENT_SPAN_ID_HEADER
from inkah.utils import is_installed, generate_id


class Inkah(object):
    def __init__(self, app=None, **kwargs):
        self._options = kwargs
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        self.monkey_patch_requests()
        app.before_request(self.before_request)
        app.after_request(self.after_request)

    def before_request(self):
        trace_id = request.headers.get(TRACE_ID_HEADER)
        span_id = request.headers.get(SPAN_ID_HEADER)
        parent_span_id = request.headers.get(PARENT_SPAN_ID_HEADER)
        span = Span(trace_id, span_id, parent_span_id)
        g.inkah_span = span

    def after_request(self, response):
        g.inkah_span.complete()
        return response

    def requests_header_injector(self, wrapped, instance, args, kwargs):
        headers = kwargs.pop('headers', None) or {}
        span_id = generate_id()
        headers.update({
            TRACE_ID_HEADER: g.inkah_span.trace_id,
            SPAN_ID_HEADER: span_id,
            PARENT_SPAN_ID_HEADER: g.inkah_span.span_id,
        })
        g.inkah_span.begin_request(span_id)
        resp = wrapped(*args, headers=headers, **kwargs)
        g.inkah_span.complete_request(span_id)
        return resp

    def monkey_patch_requests(self):
        if is_installed('requests'):
            wrapt.wrap_function_wrapper('requests', 'get', self.requests_header_injector)
            wrapt.wrap_function_wrapper('requests', 'head', self.requests_header_injector)
            wrapt.wrap_function_wrapper('requests', 'post', self.requests_header_injector)
            wrapt.wrap_function_wrapper('requests', 'patch', self.requests_header_injector)
            wrapt.wrap_function_wrapper('requests', 'put', self.requests_header_injector)
            wrapt.wrap_function_wrapper('requests', 'delete', self.requests_header_injector)
            wrapt.wrap_function_wrapper('requests', 'options', self.requests_header_injector)
