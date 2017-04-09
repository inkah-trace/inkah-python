import grpc

from inkah import event_pb2
from inkah import event_pb2_grpc
from inkah.utils import generate_id

TRACE_ID_HEADER = 'Inkah-Trace-Id'
SPAN_ID_HEADER = 'Inkah-Span-Id'
PARENT_SPAN_ID_HEADER = 'Inkah-Parent-Span-Id'


class Span(object):
    def __init__(self, trace_id, span_id, parent_span_id):
        self.trace_id = trace_id or generate_id()
        self.span_id = span_id or generate_id()
        self.parent_span_id = parent_span_id
        self.begin()

    def _send_event(self, event_type, span_id=None):
        channel = grpc.insecure_channel('localhost:50051')
        stub = event_pb2_grpc.InkahStub(channel)
        span_id = span_id or self.span_id
        event = event_pb2.Event(traceId=self.trace_id, spanId=span_id,
                                parentSpanId=self.parent_span_id, eventType=event_type)
        try:
            stub.RegisterEvent(event)
        except grpc._channel._Rendezvous as err:
            print err

    def begin(self):
        self._send_event('SPAN_BEGIN')

    def complete(self):
        self._send_event('SPAN_END')

    def begin_request(self, span_id):
        self._send_event('REQUEST_BEGIN', span_id)

    def complete_request(self, span_id):
        self._send_event('REQUEST_END', span_id)

    def annotate(self):
        pass
