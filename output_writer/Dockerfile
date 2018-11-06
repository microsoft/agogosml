# Base container
FROM python:3.7-alpine3.8 AS base

# Install dependencies
RUN mkdir /install

WORKDIR /install

COPY requirements.txt /requirements.txt

RUN pip install --install-option="--prefix=/install" -r /requirements.txt

WORKDIR /output-app
COPY . /output-app

# Tests
# run linters, setup and tests
FROM base AS test
COPY . .
# RUN  <TBD...>

# Run
FROM base AS release

COPY --from=base /install /usr/local
COPY . .

EXPOSE 5000

CMD ["python", "writer.py"]
