FROM python:3.12.3-slim-bookworm

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
    locales

COPY . /usr/src/app/

RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt