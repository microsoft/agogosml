ARG PYTHON_VERSION=3.7.0-alpine3.8

FROM python:${PYTHON_VERSION} as base-deps

# Install librdkafka dependencies 
RUN apk add --no-cache --update --virtual .build-deps \
    bash \
    libressl-dev \
    musl-dev \
    zlib-dev \
    git \
    make\
    cmake \
    g++ \ 
    libffi-dev

# Install librdkafka
ARG KAFKA_VERSION=v0.11.6
WORKDIR /root
RUN git clone -b ${KAFKA_VERSION} --single-branch https://github.com/edenhill/librdkafka.git
WORKDIR /root/librdkafka
RUN /root/librdkafka/configure && make && make install

FROM base-deps as builder

WORKDIR /usr/src/agogosml

ENV PYTHONUNBUFFERED=1

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN make clean && \
    make lint && \
    make test && \
    # make test-all && \ <- FIXME: Tox is broken.
    make docs && \
    make dist

FROM builder as agogosml

RUN pip install --no-cache-dir /usr/src/agogosml/dist/agogosml-*.tar.gz && \
    rm -rf /usr/src/agogosml && \
    rm -rf /root/librdkafka && \
    apk del .build-deps
