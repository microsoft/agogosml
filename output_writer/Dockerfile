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

WORKDIR /root
RUN git clone -b v0.11.6 --single-branch https://github.com/edenhill/librdkafka.git
WORKDIR /root/librdkafka
RUN /root/librdkafka/configure && make && make install

WORKDIR /root/output-writer
COPY . /root/output-writer

RUN apk del .build-deps

FROM base AS tests

WORKDIR /root/output-writer
COPY --from=base /root/output-writer /root/output-writer

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

# Run tests, linter
RUN pytest test_outputWriter.py
RUN pytest test_outputWriterServiceResolver.py
RUN pylint *.py

# Release
FROM base AS release
WORKDIR /root/output-writer
COPY --from=base /root/output-writer /root/output-writer
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
