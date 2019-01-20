from optionalgrpc import Service


@Service(rpc_servicer = client_pb2_grpc.add_AssemblerServicer_to_server,
         stub = assembler_pb2_grpc.AssemblerStub,
         port = 1000)
class Foo():
    pass