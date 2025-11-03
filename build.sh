#!/usr/bin/env bash

uv run manage.py makemigrations
uv run manage.py migrate
mkdir static staticfiles
uv sync --frozen && uv cache prune --ci
