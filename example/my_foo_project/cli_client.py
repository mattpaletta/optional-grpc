import logging
from typing import Iterator

from my_foo_project.foo import Foo
from my_foo_project.client import foo_pb2
from optionalgrpc import IS_RUNNING_LOCAL


def run_sample_client(configs):
    # Here's an example client.

    # We want a client API, so we set `server = False`
    client = Foo(configs = configs, server = False, use_rpc = not IS_RUNNING_LOCAL)

    method_options = ["unary", "stream", "bistream"]

    method = input("Please choose function: [{0}] > ".format(",".join(method_options)))
    if method not in method_options:
        logging.error("Invalid method: {0}".format(method))
        exit(1)

    msg_num = 0

    # here I'm reusing the definitions from the list so I don't make typing errors
    if method == method_options[0]:
        msg_to_send = input("U: > ")
        resp: foo_pb2.MyMessage = client.sendUnary(request = foo_pb2.MyMessage(num = msg_num, contents = msg_to_send))
        logging.info("Sent: {0}".format(msg_to_send))
        logging.info("Received: (#{0}) `{1}`".format(resp.num, resp.contents))

    elif method == method_options[1]:
        def helper():
            print("Sending stream, type `done` to finish.")
            msg_to_send = input("S: > ")

            msg_num = 0

            while msg_to_send != "done":
                yield foo_pb2.MyMessage(num = msg_num, contents = msg_to_send)
                msg_num += 1
                msg_to_send = input("S: > ")

        msg_generator = helper()
        resp: foo_pb2.MyMessage = client.sendStream(request_iterator = msg_generator)

        logging.info("Received: (#{0}) `{1}`".format(resp.num, resp.contents))

    elif method == method_options[2]:
        def helper():
            print("Sending/Receiving stream, type `done` to finish.")
            msg_to_send = input("B: > ")

            msg_num = 0

            while msg_to_send != "done":
                yield foo_pb2.MyMessage(num = msg_num, contents = msg_to_send)
                msg_num += 1
                msg_to_send = input("B: > ")

        msg_generator = helper()
        resps: Iterator[foo_pb2.MyMessage] = client.sendBiStream(request_iterator = msg_generator)

        for resp in resps:
            logging.info("Received: (#{0}) `{1}`".format(resp.num, resp.contents))
