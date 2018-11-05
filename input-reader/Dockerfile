FROM python:3.7-alpine3.8

# Install librdkafka
RUN apk add --no-cache --virtual .build-deps \
    bash \
    g++ \
    libressl-dev \
    make \
    musl-dev \
    zlib-dev \
    git \
    libffi-dev \
    cmake

WORKDIR /root
RUN git clone https://github.com/edenhill/librdkafka.git
WORKDIR /root/librdkafka
RUN /root/librdkafka/configure && make &&  make install

# Install Azure event hub
RUN pip install azure-eventhub

RUN apk del .build-deps
