import grpc

from inkah import event_pb2
from inkah import event_pb2_grpc
from inkah.utils import generate_id


class Span(object):
    def __init__(self, trace_id, parent_span_id, request_id):
        self.id = generate_id()
        self.trace_id = trace_id or generate_id()
        self.parent_span_id = parent_span_id
        self.request_id = request_id
        self.begin()

    def begin(self):
        channel = grpc.insecure_channel('localhost:50051')
        stub = event_pb2_grpc.InkahStub(channel)
        event = event_pb2.Event(traceId=self.trace_id, spanId=self.id, parentSpanId=self.parent_span_id, eventType='SPAN_BEGIN', requestId=self.request_id)
        stub.RegisterEvent(event)

    def complete(self):
        channel = grpc.insecure_channel('localhost:50051')
        stub = event_pb2_grpc.InkahStub(channel)
        event = event_pb2.Event(traceId=self.trace_id, spanId=self.id, parentSpanId=self.parent_span_id, eventType='SPAN_END', requestId=self.request_id)
        stub.RegisterEvent(event)

    def begin_request(self, request_id):
        channel = grpc.insecure_channel('localhost:50051')
        stub = event_pb2_grpc.InkahStub(channel)
        event = event_pb2.Event(traceId=self.trace_id, spanId=self.id, requestId=request_id, eventType='REQUEST_BEGIN')
        stub.RegisterEvent(event)

    def complete_request(self, request_id):
        channel = grpc.insecure_channel('localhost:50051')
        stub = event_pb2_grpc.InkahStub(channel)
        event = event_pb2.Event(traceId=self.trace_id, spanId=self.id, requestId=request_id, eventType='REQUEST_END')
        stub.RegisterEvent(event)

    def annotate(self):
        pass
