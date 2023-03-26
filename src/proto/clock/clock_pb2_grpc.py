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
        self.get_time = channel.unary_unary(
            "/ClockService/get_time",
            request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            response_deserializer=clock__pb2.FetchClockResponse.FromString,
        )
        self.set_offset = channel.unary_unary(
            "/ClockService/set_offset",
            request_serializer=clock__pb2.AdjustClockRequest.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )


class ClockServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def get_time(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def set_offset(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_ClockServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "get_time": grpc.unary_unary_rpc_method_handler(
            servicer.get_time,
            request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            response_serializer=clock__pb2.FetchClockResponse.SerializeToString,
        ),
        "set_offset": grpc.unary_unary_rpc_method_handler(
            servicer.set_offset,
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
    def get_time(
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
            "/ClockService/get_time",
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
    def set_offset(
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
            "/ClockService/set_offset",
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