ARG PYTHON_VERSION=3.7.0-alpine3.8

FROM python:${PYTHON_VERSION} as builder

WORKDIR /usr/src/sample_app
COPY ./sample_app /usr/src/sample_app

RUN pip install -r requirements-dev.txt

# Run tests, linter
RUN pytest testapp.py
RUN pylint *.py

# Release 
ARG PYTHON_VERSION=3.7.0-alpine3.8

FROM python:${PYTHON_VERSION}

WORKDIR /sample_app
COPY --from=builder /usr/src/sample_app /sample_app
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
