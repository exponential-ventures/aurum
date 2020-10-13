FROM python:3.7-slim

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/"

RUN pip install --upgrade pip

RUN apt-get update && apt-get install gcc python3-dev -y

COPY . /usr/src/app/

WORKDIR /usr/src/app/

RUN python3 setup.py sdist

RUN pip install .

