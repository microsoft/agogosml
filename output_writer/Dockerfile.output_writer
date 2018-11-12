FROM agogosml/agogosml as builder

# Copy the app
WORKDIR /usr/src/agogosml
COPY ./output_writer ./output_writer
COPY ./tests/ ./tests

#RUN pip install pytest pytest-runner pylint && \
#    pylint ./output_writer/*.py && \
#    pytest ./tests/*.py

# Release
FROM agogosml/agogosml AS output_writer

WORKDIR /output_writer
COPY --from=builder /usr/src/agogosml/output_writer /output_writer

CMD ["python", "main.py"]
