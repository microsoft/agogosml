ARG PYTHON_VERSION=3.7.0-alpine3.8

FROM python:${PYTHON_VERSION} as builder

RUN apk add --update make \ 
    cmake \
    g++

WORKDIR /usr/src/agogosml_cli

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install --deploy --dev 
    # --deploy causes pipenv to fail if the lock file is out of date

COPY . .

RUN pipenv run make clean && \
    pipenv run make lint && \
    pipenv run make test &&  \
    # pipenv run make test-all && \ <- FIXME: Tox is broken, no py3.5, 3.6 interpreter in image
    pipenv run make coverage && \
    pipenv run make docs && \
    pipenv run make dist

FROM python:${PYTHON_VERSION}
ENV PYTHONUNBUFFERED=1

COPY --from=builder /usr/src/agogosml_cli/dist /dist

RUN apk add --no-cache --update --virtual .build-deps \
    make cmake g++

RUN pip install /dist/agogosml_cli-*.tar.gz

RUN apk del .build-deps

ENTRYPOINT ["agogosml"]
