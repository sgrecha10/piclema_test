FROM python:3.8.10-alpine3.14

ENV PYTHONUNBUFFERED=1 \
   LANG=ru_RU.UTF-8 \
   LANGUAGE=ru_RU:ru \
   LC_ALL=ru_RU.UTF-8 \
   DEBUG=true \
   TERM=xterm-256color

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apk add --no-cache --virtual .build-deps \
   gcc\
   g++\
   postgresql-dev\
   linux-headers\
   libffi-dev
RUN python -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt --no-cache-dir
