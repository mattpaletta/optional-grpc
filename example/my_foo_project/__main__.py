import logging
import os
import sys
from typing import Iterator

import grpc

from configs.parser import Parser
from optionalgrpc import ONE_DAY_IN_SECONDS, IS_RUNNING_LOCAL


def main():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)s]')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    this_dir, _ = os.path.split(__file__)
    DATA_PATH = os.path.join(this_dir, "resources", "argparse.yml")
    configs = Parser(argparse_file = DATA_PATH).get()

    start_with_rpc = configs["mode"] == "cluster"  # Use RPC if in cluster mode.

    service_configs = {"configs": configs, "server": True, "use_rpc": start_with_rpc}

    import pprint
    pp = pprint.PrettyPrinter(indent = 4)
    logging.info("Starting server with configs: " + pp.pformat(configs))

    server: grpc.Server = None

    if configs["service"] == "foo":
        from my_foo_project.foo import Foo
        server = Foo(**service_configs)

    elif configs["service"] == "client":
        from my_foo_project.cli_client import run_sample_client
        run_sample_client(configs)
        exit(0)
    else:
        logging.debug("Unknown service: {0}".format(configs["service"]))
        exit(1)

    server.start()
    try:
        import time
        while True:
            time.sleep(ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    main()
