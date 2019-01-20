try:
    from optionalgrpc.setup import setup
    from setuptools import find_packages
    setup_tools_available = True

except ImportError:
    import ez_setup

    ez_setup.use_setuptools()
    setup_tools_available = False
    from setuptools import setup, find_packages

standard_setup_properties = {
    "name": "grpc-example",
    "version": "0.0.1",
    "url": 'https://github.com/mattpaletta',
    "packages": find_packages(),
    "include_package_data": True,
    "install_requires": ["git+git://github.com/mattpaletta/optional-grpc.git",
                      "git+git://github.com/mattpaletta/configparser.git"],
    "setup_requires": ["git+git://github.com/mattpaletta/optional-grpc.git"],
    "author": "Matthew Paletta",
    "author_email": "mattpaletta@gmail.com",
    "description": "Example python wrapper for proto libraries",
    "license": "BSD",
    "classifiers": [],
}

if setup_tools_available:
    # This one is from the optional_grpc setup class
    setup(proto_root = "my_foo_project", **standard_setup_properties)
else:
    # This is the default, in case optional_grpc is not installed yet.
    setup(**standard_setup_properties)
