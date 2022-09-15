#!/usr/bin/env bash

docker exec \
  -it mpulse-challenge-env \
  poetry run pytest .
