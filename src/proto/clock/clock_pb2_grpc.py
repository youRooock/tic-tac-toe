# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import clock_pb2 as clock__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class ClockServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.fetch_clock = channel.unary_unary(
            "/ClockService/fetch_clock",
            request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            response_deserializer=clock__pb2.FetchClockResponse.FromString,
        )
        self.adjust_clock = channel.unary_unary(
            "/ClockService/adjust_clock",
            request_serializer=clock__pb2.AdjustClockRequest.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )


class ClockServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def fetch_clock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def adjust_clock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_ClockServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "fetch_clock": grpc.unary_unary_rpc_method_handler(
            servicer.fetch_clock,
            request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            response_serializer=clock__pb2.FetchClockResponse.SerializeToString,
        ),
        "adjust_clock": grpc.unary_unary_rpc_method_handler(
            servicer.adjust_clock,
            request_deserializer=clock__pb2.AdjustClockRequest.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler("ClockService", rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class ClockService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def fetch_clock(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/ClockService/fetch_clock",
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            clock__pb2.FetchClockResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def adjust_clock(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/ClockService/adjust_clock",
            clock__pb2.AdjustClockRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
