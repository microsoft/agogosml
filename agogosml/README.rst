========
Agogosml
========


.. image:: https://img.shields.io/pypi/v/agogosml.svg
        :target: https://pypi.python.org/pypi/agogosml

.. image:: https://readthedocs.org/projects/agogosml/badge/?version=latest
        :target: https://agogosml.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

Dockerfile Instructions
    Build using:
        * docker build -t agogosml/agogosml -f agogosml/Dockerfile.agogosml agogosml
        * docker build -t agogosml/input_reader -f input_reader/Dockerfile.input_reader .
        * docker build -t agogosml/output_writer -f output_writer/Dockerfile.output_writer .
    Run using:
        * docker run agogosml/input_reader:latest
        * docker run agogosml/output_writer:latest

    Sample config:
        * docker network create testnetwork
        * docker run --rm --network testnetwork --name test-kafka -d -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST=test-kafka --env ADVERTISED_PORT=9092 spotify/kafka
        * sleep 10
        * docker run --rm --network testnetwork --name test-input -d -e MESSAGING_TYPE=kafka -e KAFKA_TOPIC=input -e APP_HOST=test-output -e APP_PORT=8080 -e KAFKA_ADDRESS=test-kafka:9092 -e KAFKA_CONSUMER_GROUP=test agogosml/input_reader:latest
        * docker run --rm --network testnetwork --name test-output -d -e MESSAGING_TYPE=kafka -e KAFKA_TOPIC=output -e KAFKA_ADDRESS=test-kafka:9092 -e OUTPUT_WRITER_PORT=8080 agogosml/output_writer:latest
Agogosml Library


* Free software: MIT license
* Documentation: https://agogosml.readthedocs.io.

