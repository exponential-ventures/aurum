FROM python:3.7-alpine


RUN mkdir /usr/src/app


ADD src/ /usr/src/app


CMD ["python", "/usr/src/app/au"]

