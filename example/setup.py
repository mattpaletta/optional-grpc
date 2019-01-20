from distutils.command.build import build
from setuptools.command.install import install
import inspect

try:
    from setuptools import setup, find_packages

except ImportError:
    import ez_setup

    ez_setup.use_setuptools()
    from setuptools import setup, find_packages


class BuildCommand(build):
    def run(self):
        import optionalgrpc.setup
        optionalgrpc.setup.compile_proto(project_root = "my_foo_project")
        build.run(self)


class InstallCommand(install):
    def run(self):
        import optionalgrpc.setup

        optionalgrpc.setup.compile_proto(project_root = "my_foo_project")

        if not self._called_from_setup(inspect.currentframe()):
            # Run in backward-compatibility mode to support bdist_* commands.
            install.run(self)
        else:
            install.do_egg_install(self)  # OR: install.do_egg_install(self)


setup(name = "grpc-example",
      version = "0.0.1",
      url = 'https://github.com/mattpaletta',
      packages = find_packages(),
      include_package_data = True,
      install_requires = [],
      setup_requires = ["optional-grpc", "configparser"],
      author = "Matthew Paletta",
      author_email = "mattpaletta@gmail.com",
      description = "Example python wrapper for proto libraries",
      license = "BSD",
      classifiers = [],
      cmdclass = {
          "build": BuildCommand,
          "install": InstallCommand,
      }
)