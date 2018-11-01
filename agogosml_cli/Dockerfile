FROM python:3.7-stretch as build

WORKDIR /usr/src/agogosml_cli
COPY . .

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --dev

RUN pipenv run make clean && \
    pipenv run make lint && \
    pipenv run make test && \
    # pipenv run make test-all <- FIXME: Tox is broken.
    pipenv run make coverage && \
    pipenv run make docs
