# Base image
FROM python:3.7-alpine3.8 AS base

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

# Install librdkafka
WORKDIR /root
RUN git clone -b v0.11.6 --single-branch https://github.com/edenhill/librdkafka.git
WORKDIR /root/librdkafka
RUN /root/librdkafka/configure && make && make install

RUN rm -rf /root/librdkafka

# Copy the app and the common modules
WORKDIR /input_reader
COPY ./input_reader /input_reader
COPY ./agogosml/agogosml/streaming_client/ /agogosml/agogosml/streaming_client

# Install needed production requirements
RUN pip install -r requirements.txt

FROM base AS tests

WORKDIR /input_reader
COPY --from=base /input_reader /input_reader
COPY --from=base /agogosml/agogosml/streaming_client /agogosml/agogosml/streaming_client
COPY ./tests/ /tests

# Install testing requirements
RUN pip install -r requirements-dev.txt

# Run tests, linter
WORKDIR /
RUN python -m pylint input_reader/

RUN python -m pytest tests/test_inputReader.py

# Release
FROM base AS release

WORKDIR /input_reader

COPY --from=base /input_reader /input_reader
COPY --from=base /agogosml/agogosml/streaming_client /agogosml/agogosml/streaming_client

# Cleanup
RUN apk del .build-deps

CMD ["python", "main.py"]