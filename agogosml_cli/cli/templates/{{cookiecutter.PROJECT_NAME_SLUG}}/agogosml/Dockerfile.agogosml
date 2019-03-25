ARG PYTHON_VERSION=3.7.0
ARG LIBRDKAFKA_VERSION=0.11.6
FROM ucalgary/python-librdkafka:${PYTHON_VERSION}-${LIBRDKAFKA_VERSION}

ENV PYTHONUNBUFFERED=1

ARG AGOGOSML_VERSION={{cookiecutter.AGOGOSML_CLI_VERSION}}
RUN apk add --no-cache --update --virtual .build-deps \
    g++ \
    libffi-dev \
    libressl-dev \
    cmake \
    make \
 && pip install --no-cache-dir agogosml==${AGOGOSML_VERSION} \
 && apk del .build-deps
