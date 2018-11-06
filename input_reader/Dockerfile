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

WORKDIR /root/input_reader
COPY . /root/input_reader

RUN apk del .build-deps

FROM base AS tests

WORKDIR /root/input_reader
COPY --from=base /root/input_reader /root/input_reader

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

# Run tests, linter
RUN pytest test_input_reader.py
#RUN pylint *.py

# Release
FROM base AS release
WORKDIR /root/input_reader
COPY --from=base /root/input_reader /root/input_reader
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
