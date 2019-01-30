ARG PYTHON_VERSION=3.7.0-alpine3.8

FROM python:${PYTHON_VERSION} as builder

WORKDIR /usr/src/{{cookiecutter.PROJECT_NAME_SLUG}}

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

# Run tests, linter
RUN pytest testapp.py \
 && isort --check-only *.py \
 && flake8 *.py

# Release
FROM python:${PYTHON_VERSION}

WORKDIR /{{cookiecutter.PROJECT_NAME_SLUG}}
COPY --from=builder /usr/src/{{cookiecutter.PROJECT_NAME_SLUG}} /{{cookiecutter.PROJECT_NAME_SLUG}}
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
