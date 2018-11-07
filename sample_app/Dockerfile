# Base image
FROM python:3.7-alpine3.8 AS base

WORKDIR /sample_app
COPY . /sample_app

RUN pip install -r requirements.txt

# Tests image
FROM base as tests

COPY --from=base /sample_app /sample_app

RUN pip install -r requirements-dev.txt

# Run tests, linter
RUN python -m pytest testapp.py
RUN python -m pylint *.py

# Release image
FROM base
COPY --from=base /sample_app /sample_app