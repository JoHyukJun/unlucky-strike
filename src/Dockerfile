FROM arm32v5/python:3.11-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    ninja-build \
    cmake \
    postgresql \
    gcc \
    python3-dev \
    musl-dev \
    git \
    locales \
    zlib1g \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev

COPY . /usr/src/app/

RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt