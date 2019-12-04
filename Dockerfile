FROM python:3.7-alpine


RUN apk add --no-cache --update build-base gcc git bash python python-dev

RUN mkdir /usr/src/app


ADD . /usr/src/app

WORKDIR /usr/src/app
RUN pip install .

ENTRYPOINT ["au"]

