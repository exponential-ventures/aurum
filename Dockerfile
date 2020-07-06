FROM python:3.7-alpine

RUN apk add --no-cache --update build-base gcc git bash  util-linux linux-headers

RUN mkdir /usr/src/app

ADD requirements.txt /usr/src/app

WORKDIR /usr/src/app

RUN pip install -r requirements.txt

ADD . /usr/src/app

RUN pip install .
