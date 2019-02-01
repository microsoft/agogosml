ARG PYTHON_VERSION=3.7.0-alpine3.8

FROM python:${PYTHON_VERSION} as builder

RUN apk add --update make \ 
    cmake \
    g++

WORKDIR /usr/src/agogosml_cli

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN make clean && \
    make lint && \
    make test && \
    # make test-all && \ <- FIXME: Tox is broken, no py3.5, 3.6 interpreter in image
    make docs && \
    make dist

FROM python:${PYTHON_VERSION}
ENV PYTHONUNBUFFERED=1

COPY --from=builder /usr/src/agogosml_cli/dist /dist

# G++ is a runtime dependency if you want to be able to use this docker container
RUN apk add --no-cache --update --virtual .build-deps make cmake && \
    apk add --no-cache --update --virtual .rt-deps g++ && \
    pip install --no-cache-dir /dist/agogosml_cli-*.tar.gz && \
    apk del .build-deps

WORKDIR /home

ENTRYPOINT ["agogosml"]
