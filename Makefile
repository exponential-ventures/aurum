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


.PHONY: coverage
coverage:
	docker run -it --rm --name aurum k2so.xnv.io/aurum:latest /bin/bash -c "pip install coverage && coverage run -m unittest discover -v -f  tests && coverage report"

.PHONY: ssh
ssh:
	docker run -it --rm --name aurum k2so.xnv.io/aurum:latest /bin/bash
