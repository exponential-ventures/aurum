.PHONY: build
build:
	docker build -t k2so.xnv.io/aurum .

.PHONY: tests
tests:
	docker run -it --rm --name aurum k2so.xnv.io/aurum:latest python -m unittest discover -v -f  tests

# Run specific tests by calling like such:
# make test_name=tests.test_au_command unit-test
.PHONY: unit-test
unit-test:
	docker run -it --rm --name aurum k2so.xnv.io/aurum:latest python  -m unittest -v $(test_name)

.PHONY: ssh
ssh:
	docker run -it --rm --name aurum k2so.xnv.io/aurum:latest /bin/bash


.PHONY: au
au:
	docker run -it --rm --name aurum k2so.xnv.io/aurum:latest au


.PHONY: example
example:
	docker run -it --rm --name aurum k2so.xnv.io/aurum:latest /bin/bash -c "au init && examples/src/experiment.py -v -n"

build_package:
	docker run -v $(shell pwd):/usr/src/app -it --rm k2so.xnv.io/aurum python3 setup.py sdist bdist_wheel
	scp -r dist/* robot@l337:/home/robot/pypi_server/packages
	sudo rm -rf build/ dist/ aurum.egg-info
