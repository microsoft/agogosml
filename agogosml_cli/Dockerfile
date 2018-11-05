ARG PYTHON_VERSION=3.7.0-alpine3.8

FROM python:${PYTHON_VERSION} as builder

WORKDIR /usr/src/agogosml_cli
COPY . .

RUN apk add --update make && \ 
    pip install pipenv && \
    pipenv install --dev

RUN pipenv run make clean && \
    pipenv run make lint && \
    # pipenv run make test && \ <-- FIXME: Tests relying on modified time not reliable in docker build, unfortunately
    # pipenv run make test-all <- FIXME: Tox is broken.
    pipenv run make coverage && \
    pipenv run make docs && \
    pipenv run make dist

FROM python:${PYTHON_VERSION}
ENV PYTHONUNBUFFERED=1

COPY --from=builder /usr/src/agogosml_cli/dist /

RUN pip install /agogosml_cli-0.1.0.tar.gz

ENTRYPOINT ["agogosml" ]