FROM python:3.7-alpine3.8

WORKDIR /usr/src/agogosml_cli
COPY . .

RUN apk add --update make && \ 
    pip install pipenv && \
    pipenv install --dev

RUN pipenv run make clean && \
    pipenv run make lint && \
    pipenv run make test && \
    # pipenv run make test-all <- FIXME: Tox is broken.
    pipenv run make coverage && \
    pipenv run make docs
