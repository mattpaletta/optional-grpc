from typing import Dict, Iterator
from grpc import RpcContext
from optionalgrpc.service import Service

from my_foo_project.client import foo_pb2_grpc, foo_pb2


@Service(rpc_servicer = foo_pb2_grpc.add_FooServicer_to_server,
         stub = foo_pb2_grpc.FooStub,
         port = 1000)
class Foo(foo_pb2_grpc.FooServicer):
    def __init__(self, configs: Dict[str, any], server=False, use_rpc=False):
        self.configs = configs
        self.server = server
        self.use_rpc = use_rpc

    def sendUnary(self, request: foo_pb2.MyMessage, context: RpcContext = None) -> foo_pb2.MyMessage:
        msg_num = request.num
        msg_contents = request.contents

        total_num_messages = 1
        message_char_length = len(msg_contents)

        resp = "Received message.  It had number: {0}.  It had {1} characters.".format(msg_num,
                                                                                       message_char_length)
        return foo_pb2.MyMessage(num = total_num_messages, contents = resp)

    def sendStream(self, request_iterator: Iterator[foo_pb2.MyMessage], context: RpcContext = None) -> foo_pb2.MyMessage:
        total_num_messages = 0
        message_sum = 0
        message_char_length = 0
        for msg in request_iterator:
            msg_num = msg.num
            msg_contents = msg.contents

            total_num_messages += 1
            message_sum += msg_num
            message_char_length += len(msg_contents)

        resp = "Received: {0} messages.  They add up to: {1}.  They had {2} characters.".format(total_num_messages,
                                                                                                message_sum,
                                                                                                message_char_length)
        return foo_pb2.MyMessage(num = total_num_messages, contents = resp)

    def sendBiStream(self, request_iterator: Iterator[foo_pb2.MyMessage], context: RpcContext = None) -> Iterator[foo_pb2.MyMessage]:
        for msg in request_iterator:
            msg_num = msg.num
            msg_contents = msg.contents
            yield foo_pb2.MyMessage(num = msg_num, contents = "Received: {0}".format(msg_contents))
