build:
	docker build -t aurum .

test:
	docker run -it --rm --name aurum aurum:latest python -m unittest discover -v -f  tests

ssh:
	docker run -it --rm --name aurum aurum:latest /bin/bash

clean-pyc:
	find . -path "*.pyc"  -delete