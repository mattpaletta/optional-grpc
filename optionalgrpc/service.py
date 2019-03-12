import logging
from concurrent import futures
from multiprocessing import cpu_count
from time import sleep

import grpc

from optionalgrpc import IS_RUNNING_LOCAL
from pynotstdlib.singleton import Singleton


try:
    from py_grpc_prometheus.prometheus_client_interceptor import PromClientInterceptor
    from py_grpc_prometheus.prometheus_server_interceptor import PromServerInterceptor
    from prometheus_client import start_http_server
    _prometheus_support = True

except ImportError:
    _prometheus_support = False


class Service(object):
    """
    Wrapper for GRPC Classes to allow for easy switching between using RPC calls
    (when running in a cluster) and using Singletons (when running locally).  The client
    can connect to the server at the name of the thrift_class.
    """

    def __init__(self, rpc_servicer=None, stub = None, port: int = 0, pool_size=(cpu_count() - 1), num_retries=-1,
                 metrics_port: int = 9093):
        """
        :param class rpc_servicer: Generated grpc servicer method we are wrapping.
        :param int port: The port for the rpc stub to listen on/call to.
        :param int pool_size: Only required if using a Pool Server, specifies the pool size.
        :param int num_retries: Number of times to retry connecting to a service before exiting, -1 for unlimited.
        """

        self._rpc_servicer_method = rpc_servicer

        self._metrics_port = metrics_port

        if self._rpc_servicer_method is not None:
            assert stub is not None, "Requires stub for clients."
        self._stub = stub

        self._port = port
        self._transport = None
        self._pool_size = pool_size
        self._num_retries = max(3, num_retries)

    def _get_service(self, inst, service_name: str = None):
        if _prometheus_support:
            server = grpc.server(futures.ThreadPoolExecutor(max_workers = self._pool_size),
                                                            interceptors = (PromServerInterceptor,))
            start_http_server(self._metrics_port)
        else:
            server = grpc.server(futures.ThreadPoolExecutor(max_workers = self._pool_size))
        assert self._rpc_servicer_method is not None, "Service not wrapped: {0}".format(service_name)

        self._rpc_servicer_method(inst, server)

        server.add_insecure_port('[::]:{0}'.format(self._port))
        return server

    def __call__(self, original_clazz):
        logging.debug("Wrapped " + str(original_clazz.__name__))

        decorator_self = self
        dec_name = original_clazz.__name__

        assert self._rpc_servicer_method is not None, "Must pass in servicer argument: {0}".format(dec_name)

        def wrappee(*args, **kwargs):
            logging.debug('in decorator before wrapee with flag ' + dec_name)
            assert "configs" in kwargs.keys(), "must pass configs to rpc as kwargs"
            use_rpc_configs = kwargs["configs"]["use_rpc"]

            # Only use rpc if deployed in docker.
            if use_rpc_configs == "always":
                use_rpc = True
                logging.debug("Always using RPC")
            elif use_rpc_configs == "never":
                use_rpc = False
                logging.debug("Never using RPC")
            elif use_rpc_configs in ["auto", "force"] and "use_rpc" in kwargs.keys():
                use_rpc = kwargs["use_rpc"]
                logging.debug("Using RPC from kwargs")
            elif use_rpc_configs == "auto" and not "use_rpc" in kwargs.keys():
                logging.debug("use_rpc not found in kwargs")
                use_rpc = not IS_RUNNING_LOCAL
            else:
                raise EnvironmentError("Must specify use_rpc for decorator when (--use_rpc True): " + dec_name)

            logging.debug("Using rpc ({0}): {1}".format(dec_name, use_rpc))

            if "server" not in kwargs.keys():
                use_server = False
                logging.warning("Defaulting to not start as server for: " + dec_name)
            else:
                use_server = kwargs["server"]
                logging.debug("Using server ({0}): {1} ".format(dec_name, use_server))

            if use_rpc and use_server:
                handler = original_clazz(*args, **kwargs)
                decorator_self.__inst = handler

                server = self._get_service(service_name = dec_name, inst = decorator_self.__inst)
                return server

            elif use_rpc and not use_server:
                logging.debug("Returning client channel.")
                self._transport: grpc.Channel = self.get_client_channel(dec_name)
                self._channel = self._stub(channel = self._transport)

                retries = 0
                while retries < self._num_retries:
                    try:
                        grpc.channel_ready_future(self._transport).result(timeout = 20)
                        logging.debug("Client (" + dec_name + ") connected to server")
                        return self._channel
                    except grpc.FutureTimeoutError:
                        logging.warning("Failed to connect.  Retry: " + str(retries))
                        # Add a sleep (incrementing exponentially) first so we don't immediately retry.
                        sleep(2 ** retries)
                        retries += 1

            else:
                logging.debug("Returning Singleton of class: " + dec_name)
                return Singleton(original_clazz).Instance(*args, **kwargs)

        logging.debug('in decorator after wrapee with flag ' + dec_name)
        return wrappee

    def __del__(self):
        if self._transport is not None and type(self._transport) is grpc.Channel:
            self._transport.close()

    def get_client_channel(self, service_name):
        assert self._port is not None and self._port > 0, "Invalid port."
        hostname = "{0}:{1}".format(service_name.lower(), self._port)
        logging.debug("Trying hostname: " + hostname)
        if _prometheus_support:
            channel = grpc.intercept_channel(grpc.insecure_channel(hostname),
                                             PromClientInterceptor())
            start_http_server(self._metrics_port)
        else:
            channel = grpc.insecure_channel(hostname)
        return channel
