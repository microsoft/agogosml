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

# Copy the app and the common modules
WORKDIR /root/output_writer
COPY ./output_writer /root/output_writer
COPY ./io_base/ /root/io_base

# Install needed production requirements
RUN pip install -r requirements.txt

FROM base AS tests

WORKDIR /root/output_writer
COPY --from=base /root/output_writer /root/output_writer
COPY --from=base /root/io_base /root/io_base
COPY ./tests/ /root/tests

# Install testing requirements
RUN pip install -r requirements-dev.txt

# Run tests, linter
#WORKDIR /root
#RUN pylint output_writer/*.py

# Todo: fix module load issue
#WORKDIR /root/tests
#RUN pytest test_outputWriter.py
#RUN pytest test_outputWriterServiceResolver.py


# Release
FROM base AS release

WORKDIR /root/output_writer

COPY --from=base /root/output_writer /root/output_writer
COPY --from=base /root/io_base /root/io_base

# Cleanup
RUN apk del .build-deps

CMD ["python", "main.py"]