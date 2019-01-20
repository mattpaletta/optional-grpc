from distutils.command.build import build
from distutils.command.install import install

try:
    from setuptools import setup as default_setup, find_packages
except ImportError:
    import ez_setup

    ez_setup.use_setuptools()
    from setuptools import setup as default_setup, find_packages


# We can export this in case anybody wants to use it for something else
def compile_proto(project_root):
    import subprocess
    import os
    import sys

    for root, dir, files in os.walk(project_root):
        for file in files:
            should_compile = False
            if os.path.exists(os.path.join(root, ".protolang")):
                with open(os.path.join(root, ".protolang"), "r") as protolang:
                    for line in protolang:
                        if line == "python" or line == "py":
                            should_compile = True

            if should_compile and str(file).endswith(".proto"):
                print("Compiling: " + os.path.join(root, file))
                cmd = "{0} -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. --mypy_out=. {1}".format(
                                    sys.executable.split("/")[-1],
                                    os.path.join(root, file))
                print(cmd)
                ret = subprocess.call([cmd], shell=True)
                if ret != 0:
                    print("Failed to compile proto files.")
                    exit(ret)


# class _BuildCommand(build):
#     def run(self, project_root: str = None):
#         compile_proto(project_root)
#         build.run(self)
#
#
# class _InstallCommand(install):
#     def run(self, project_root: str = None):
#         compile_proto(project_root)  # TODO:// Don't recompile if don't need to
#         import inspect
#
#         if not self._called_from_setup(inspect.currentframe()):
#             # Run in backward-compatibility mode to support bdist_* commands.
#             install.run(self)
#         else:
#             install.do_egg_install(self)  # OR: install.do_egg_install(self)


# def setup(proto_root: str = None, **kwargs):
#     # If not proto_root is set, we simply do nothing.
#     if proto_root is not None and proto_root != "":
#         if "cmdclass" in kwargs.keys():
#             if "build" in kwargs["cmdclass"]:
#                 assert issubclass(kwargs["cmdclass"]["build"], _BuildCommand), \
#                     "You must subclass the Build class in your setup file"
#
#             else:
#                 kwargs["cmdclass"]["build"] = _BuildCommand
#
#             if "install" in kwargs["cmdclass"]:
#                 assert issubclass(kwargs["cmdclass"]["install"], _InstallCommand), \
#                     "You must subclass the Install class in your setup file"
#
#             else:
#                 kwargs["cmdclass"]["install"] = _InstallCommand
#         else:
#             # If it's not set, we monkeypatch it.
#             kwargs["cmdclass"] = {
#                 "build": _InstallCommand,
#                 "install": _InstallCommand
#             }
#
#     default_setup(**kwargs)
