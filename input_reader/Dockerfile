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

ENV C_INCLUDE_PATH /root/librdkafka/src
ENV LIBRARY_PATH /root/librdkafka/src
ENV LD_LIBRARY_PATH /root/librdkafka/src


WORKDIR /root
RUN git clone https://github.com/Parsely/pykafka.git
WORKDIR /root/pykafka
RUN python setup.py develop

# Install Azure event hub
RUN pip install azure-eventhub

RUN apk del .build-deps

COPY . /root/src
WORKDIR /root/src

# kafka zookeeper ports
EXPOSE 9092
EXPOSE 2128 
ENTRYPOINT ["python", "simple_kafka.py"]