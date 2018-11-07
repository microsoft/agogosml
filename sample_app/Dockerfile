# Base image
FROM python:3.7-alpine3.8 AS base

WORKDIR /sample_app
COPY . /sample_app

RUN pip install -r requirements-dev.txt

# Run tests, linter
RUN pytest testapp.py
RUN pylint *.py

# Release 
FROM python:3.7-alpine3.8
WORKDIR /sample_app
COPY --from=base /sample_app /sample_app
RUN pip install -r requirements.txt

CMD ["python", "placeholder.py"]