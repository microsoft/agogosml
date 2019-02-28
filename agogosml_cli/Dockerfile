ARG PYTHON_VERSION=3.7.2-alpine3.8

FROM python:${PYTHON_VERSION} as builder

ARG TOX_VERSION=py37
RUN echo "using tox-version: "; echo $TOX_VERSION

RUN apk add --update make \ 
    cmake \
    g++

RUN apk add \
    git \
    bash \
    build-base \
    linux-headers \
    bzip2 \
    bzip2-dev \
    sqlite-dev \
    zlib-dev \
    curl \
    libffi-dev \
    ncurses-dev \
    openssl-dev \
    readline-dev \
    tk-dev \
    xz-dev \
    zlib-dev

ENV HOME  /root
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

WORKDIR /usr/src/agogosml_cli

#see https://www.loganasherjones.com/2018/03/setting-up-your-python-environment/
RUN if [[ "$TOX_VERSION" = "all" ]]; then \
        curl https://pyenv.run | bash && \
        pyenv install 3.5.6 && \
        pyenv install 3.6.8 && \
        pyenv install 3.7.2 && \
        echo "3.5.6" >> .python-version && \
        echo "3.6.8" >> .python-version && \
        echo "3.7.2" >> .python-version; \
    fi

RUN pip install pytest tox
RUN pip install tox-globinterpreter

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN make clean && \
    make lint && \
    make test && \
    make test-single && \
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
