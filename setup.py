try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup

    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

setup(
    name="optional-grpc",
    version="0.0.1",
    url='https://github.com/mattpaletta/optional-grpc.git',
    packages=find_packages(),
    include_package_data=True,
    install_requires=["grpcio",
                      "grpcio-tools",
                      "mypy-protobuf",
                      "pynotstdlib"],
    author="Matthew Paletta",
    author_email="mattpaletta@gmail.com",
    description="An optional grpc wrapper for local debuggging.",
    license="BSD",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications',
    ]
)

