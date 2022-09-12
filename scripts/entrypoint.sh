#!/usr/bin/env bash

apt update
add-apt-repository ppa:deadsnakes/ppa
apt update
apt install -y software-properties-common python3 python3-pip build-essential libpq-dev
pip3 install -U poetry
poetry install
poetry run alembic upgrade head
poetry run uvicorn src.main:app --reload --host=0.0.0.0
