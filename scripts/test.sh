#!/usr/bin/env bash

docker exec \
  -e ENV=test \
  -it mpulse-challenge-env \
  poetry run pytest -v .
