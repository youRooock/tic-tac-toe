# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import proto.game.game_pb2 as game__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class GameServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.set_mark = channel.unary_unary(
                '/GameService/set_mark',
                request_serializer=game__pb2.SetMarkRequest.SerializeToString,
                response_deserializer=game__pb2.SetMarkResponse.FromString,
                )
        self.inform = channel.unary_unary(
                '/GameService/inform',
                request_serializer=game__pb2.InformRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class GameServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def set_mark(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def inform(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GameServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'set_mark': grpc.unary_unary_rpc_method_handler(
                    servicer.set_mark,
                    request_deserializer=game__pb2.SetMarkRequest.FromString,
                    response_serializer=game__pb2.SetMarkResponse.SerializeToString,
            ),
            'inform': grpc.unary_unary_rpc_method_handler(
                    servicer.inform,
                    request_deserializer=game__pb2.InformRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'GameService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class GameService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def set_mark(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/GameService/set_mark',
            game__pb2.SetMarkRequest.SerializeToString,
            game__pb2.SetMarkResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def inform(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/GameService/inform',
            game__pb2.InformRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)