FROM python:3.10.1-alpine3.15

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
   linux-headers
RUN apk add libressl-dev libffi-dev

RUN pip3 install -r /app/requirements.txt --no-cache-dir
