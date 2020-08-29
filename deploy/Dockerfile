FROM python:buster

RUN apt update && apt upgrade -y && apt install -y htop mc vim sqlite3 libsqlite3-dev

ARG PROJECT_USER
RUN adduser --disabled-password ${PROJECT_USER}
WORKDIR /home/${PROJECT_USER}

RUN mkdir pyrandseqbot
WORKDIR /home/${PROJECT_USER}/pyrandseqbot

RUN mkdir .logs db

RUN python -m pip install --upgrade pip wheel setuptools

COPY *.txt ./
RUN pip install -r requirements.txt

COPY LICENSE *.py *.in ./
COPY pyrandseqbot pyrandseqbot

RUN chown -R ${PROJECT_USER}:${PROJECT_USER} /home/${PROJECT_USER}
RUN chmod -R gu+rwx /home/${PROJECT_USER}
USER ${PROJECT_USER}
