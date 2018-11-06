# Base image
FROM python:3.7-alpine3.8 AS base

WORKDIR /output-writer
COPY . /output-writer

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

# Run tests, linter
RUN pytest test_outputWriter.py
RUN pytest test_outputWriterServiceResolver.py
RUN pylint *.py

# Release
FROM python:3.7-alpine3.8
WORKDIR /output-writer
COPY --from=base /output-writer /output-docwriter
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
