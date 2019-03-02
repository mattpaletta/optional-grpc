# optional-grpc
Run functions as GRPC function or locally with a runtime parameter

### Installation
```
pip3 install git+git://github.com/mattpaletta/optional-grpc.git
```

This is an wrapper for GRPC (in Python) that will allow you to
switch between running functions as RPC calls and running
them as normal Python objects.<br>
<br>

## To wrap a new class
1. The class must be a subclass of the GRPC servicer.
2. Wrap the function, passing in the generated thrift servicer function, as well as the stub and the desired port.
3. The initializer must be a subclass of follow the signature: `def __init__(self, configs: Dict[str, any], server=False, use_rpc=False):`<br>

```python
from typing import Dict, Union
from optionalgrpc.service import Service

from my_foo_project.client import foo_pb2_grpc


@Service(rpc_servicer = foo_pb2_grpc.add_FooServicer_to_server,
         stub = foo_pb2_grpc.FooStub,
         port = 1000)
class Foo(foo_pb2_grpc.FooServicer):
    def __init__(self, configs: Dict[str, Union[int, str]], server:bool = False, use_rpc: bool = False):
        self.configs = configs
        self.server = server
        self.use_rpc = use_rpc
```

## Using the wrapped class:
Anywhere where you initialize a server of that GRPC class, set `server = True`.  If you want to get a client, set `server = False`.
For simplicity at the moment, `configs`, `server`, and `use_rpc` must use `kwargs` in every initialization of that object.
This is enforced within the library.

For example, to create a server/client for the service `Foo`:
```python
server = Foo(configs = configs, server = True, use_rpc = not IS_RUNNING_LOCALLY)
client = Foo(configs = configs, server = False, use_rpc = not IS_RUNNING_LOCALLY)
```

If we set `use_rpc = True`, then both will be a GRPC server/client stub for the `Foo` service respectively.
If we instead set `use_rpc = False`, both will point to the same instance of the original `Foo` object, which is a singleton.<br>

You can find a more full example along with its own documentation in the `example` folder.<br>
In addition, the example contains an example of how to include generating the python API for your GRPC functions as part of
the Pip wheel process.  I also include sample commands to automatically rebuild the GRPC files as you're working.

### Motivation
I wanted to be able to test code that uses RPC on my local machine and use the IDE debugger, without
having to manage a bunch of running Python instances for the server/client RPC call.
This will allow me to test my code as one giant application bundle, but deploy using
docker, and start the server and client code separately, while retaining the same functionality.

I also wanted to be able to change between running as a cluster and running locally with simple runtime arguments.

If you're using thrift instead, you can see the related project here: [https://github.com/mattpaletta/optional-thrift](optional-thrift)

### Questions, Comments, Concerns, Queries, Qwibbles?

If you have any questions, comments, or concerns please leave them in the GitHub
Issues tracker:

https://github.com/mattpaletta/optional-thrift/issues

### Bug reports

If you discover any bugs, feel free to create an issue on GitHub. Please add as much information as
possible to help us fixing the possible bug. We also encourage you to help even more by forking and
sending us a pull request.

https://github.com/mattpaletta/optional-grpc/issues

## Maintainers

* Matthew Paletta (https://github.com/mattpaletta)

## License

MIT License. Copyright 2019 Matthew Paletta. http://mrated.ca