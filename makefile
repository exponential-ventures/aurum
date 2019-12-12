.PHONY: build
build:
	docker build -t aurum .

.PHONY: tests
tests:
	docker run -it --rm --name aurum aurum:latest python -m unittest discover -v -f  tests

# Run specific tests by calling like such:
# make test_name=tests.test_au_command unit-test
.PHONY: unit-test
unit-test:
	docker run -it --rm --name aurum aurum:latest python  -m unittest -v $(test_name)

.PHONY: ssh
ssh:
	docker run -it --rm --name aurum aurum:latest /bin/bash


.PHONY: au
au:
	docker run -it --rm --name aurum aurum:latest au