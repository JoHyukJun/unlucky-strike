FROM python:3.10.4

WORKDIR /usr/src/app

ENV PYTHONDOWNTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev zlib-dev jpeg-dev

COPY . /usr/src/app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt