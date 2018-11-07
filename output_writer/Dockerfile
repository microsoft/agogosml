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
WORKDIR /output_writer
COPY ./output_writer /output_writer
COPY ./agogosml/agogosml/streaming_client/ /agogosml/agogosml/streaming_client

# Install needed production requirements
RUN pip install -r requirements.txt

FROM base AS tests

WORKDIR /output_writer
COPY --from=base /output_writer /output_writer
COPY --from=base /agogosml/agogosml/streaming_client /agogosml/agogosml/streaming_client
COPY ./tests/ /tests

# Install testing requirements
RUN pip install -r requirements-dev.txt

# Run tests, linter
WORKDIR /
RUN python -m pylint output_writer/*.py

RUN python -m pytest tests/test_outputWriter.py
RUN python -m pytest tests/test_outputWriterServiceResolver.py

# Release
FROM base AS release

WORKDIR /output_writer

COPY --from=base /output_writer /output_writer
COPY --from=base /agogosml/agogosml/streaming_client /agogosml/agogosml/streaming_client

# Cleanup
RUN apk del .build-deps

CMD ["python", "main.py"]