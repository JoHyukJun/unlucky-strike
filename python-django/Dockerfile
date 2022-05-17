FROM python:3.10.4-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDOWNTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    cmake \
    postgresql \
    gcc \
    python3-dev \
    musl-dev \
    git \
    locales

COPY . /usr/src/app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt