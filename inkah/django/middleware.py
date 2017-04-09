from threading import local

import wrapt

from inkah import Span, TRACE_ID_HEADER, SPAN_ID_HEADER, PARENT_SPAN_ID_HEADER
from inkah.utils import is_installed, generate_id

_thread_locals = local()


class TracingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.monkey_patch_requests()

    def __call__(self, request):
        trace_id = request.META.get(TRACE_ID_HEADER)
        span_id = request.META.get(SPAN_ID_HEADER)
        parent_span_id = request.META.get(PARENT_SPAN_ID_HEADER)
        span = Span(trace_id, span_id, parent_span_id)
        request.inkah_span = span

        _thread_locals.request = request

        response = self.get_response(request)

        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request

        span.complete()
        request.inkah_span = None

        return response

    def requests_header_injector(self, wrapped, instance, args, kwargs):
        headers = kwargs.pop('headers', None) or {}
        span_id = generate_id()
        current_span = _thread_locals.request.inkah_span
        headers.update({
            TRACE_ID_HEADER: current_span.trace_id,
            SPAN_ID_HEADER: span_id,
            PARENT_SPAN_ID_HEADER: current_span.span_id,
        })
        current_span.begin_request(span_id)
        resp = wrapped(*args, headers=headers, **kwargs)
        current_span.complete_request(span_id)
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
