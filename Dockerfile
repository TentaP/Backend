# syntax=docker/dockerfile:1
# For use with parent project
# https://github.com/TentaP/TentaP

From python:3.10.7-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /srv/app

COPY ./requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install -r requirements.txt 

COPY ./entrypoint.sh .

COPY . .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["/srv/app/entrypoint.sh"]
