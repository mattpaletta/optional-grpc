build:
	pip3 install git+git://github.com/mattpaletta/optional-grpc.git
	python3 setup.py build

watch:
	watchman-make -p '**/*.proto' --run "python3 setup.py build"