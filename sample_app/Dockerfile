# Base image
FROM python:3.7-alpine3.8 AS base

WORKDIR /instance-app
COPY . /instance-app

RUN pip install -r requirements-dev.txt

# Run tests, linter
RUN pytest testapp.py
RUN pylint *.py

# Release 
FROM python:3.7-alpine3.8
WORKDIR /instance-app
COPY --from=base /instance-app /instance-app
RUN pip install -r requirements.txt

CMD ["python", "placeholder.py"]