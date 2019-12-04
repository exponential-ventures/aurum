FROM python:3.7-alpine


RUN mkdir /usr/src/app


ADD . /usr/src/app

WORKDIR /usr/src/app
RUN pip install .

ENTRYPOINT ["au"]

