ARG PYTHON_VERSION=3.7.0-alpine3.8

FROM python:${PYTHON_VERSION} as builder

WORKDIR /usr/src/agogosml_cli
COPY . .

RUN apk add --update make \ 
    cmake \
    g++ && \ 
    pip install pipenv && \
    pipenv install --dev

RUN pipenv run make clean && \
    pipenv run make lint && \
    pipenv run make test &&  \
    # pipenv run make test-all && \ <- FIXME: Tox is broken, no py3.5, 3.6 interpreter in image
    pipenv run make coverage && \
    pipenv run make docs && \
    pipenv run make dist

FROM python:${PYTHON_VERSION}
ENV PYTHONUNBUFFERED=1

COPY --from=builder /usr/src/agogosml_cli/dist /

RUN pip install /agogosml_cli-*.tar.gz

ENTRYPOINT ["agogosml"]