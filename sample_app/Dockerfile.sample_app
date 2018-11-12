
# Base image
FROM agogosml/agogosml as builder

WORKDIR /usr/src/sample_app
COPY ./sample_app /usr/src/sample_app

RUN pip install -r requirements-dev.txt

# Run tests, linter
RUN pytest testapp.py
RUN pylint *.py

# Release 
FROM agogosml/agogosml
WORKDIR /sample_app
COPY --from=builder /usr/src/sample_app /sample_app
RUN pip install -r requirements.txt

CMD ["python", "main.py"]