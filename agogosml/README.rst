========
Agogosml
========

.. image:: https://img.shields.io/pypi/v/agogosml.svg
        :target: https://pypi.python.org/pypi/agogosml

.. image:: https://readthedocs.org/projects/agogosml/badge/?version=latest
        :target: https://agogosml.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Overview
--------
The agogosml package was developed to provide a Data Engineer with a simple
configurable data pipeline consisting of three components: an input reader,
sample app (that holds a trained ML model) and an output writer. The three
components are instrumented using one Docker container per component.


Input Reader
________________
The input reader acts as the data receiver and obtains the data required as
input for the ML model. The package supports both Kafka and EventHub.


Output Writer
_____________
The output writer receives the scored data from the sample app and sends it onto
a streaming client (a Kafka or Eventhub instance).


Sample App
_____________
The sample app receives data from the input reader and feeds it to the ML model
for scoring. Once scored the data is sent onto the output writer.


Docker Instructions
_________________________

Install `Docker <https://docs.docker.com/install/>`_ .

Build the base image using:

.. code:: bash

    $ docker build -t agogosml/agogosml -f agogosml/Dockerfile.agogosml agogosml

Then the input reader image:

.. code:: bash

    $ docker build -t agogosml/input_reader -f input_reader/Dockerfile.input_reader .


The sample app:

.. code:: bash

    $ docker build -t agogosml/sample_app -f sample_app/Dockerfile.sample_app .

And finally the output writer:

.. code:: bash

    $ docker build -t agogosml/output_writer -f output_writer/Dockerfile.output_writer .


A Docker network must then be created with:

.. code:: bash

    $ docker network create testnetwork

The four Docker images must then be run, prepending the parameter ``-e`` to any
environment variables. An example of how to run one of these Docker images is:

.. code:: bash

    $ docker run --rm --network testnetwork --name test-input -d -e MESSAGING_TYPE=kafka -e KAFKA_TOPIC=input -e APP_HOST=test-output -e APP_PORT=8080 -e KAFKA_ADDRESS=test-kafka:9092 -e KAFKA_CONSUMER_GROUP=test agogosml/input_reader:latest

    $ docker run --rm --network testnetwork --name test-output -d -e MESSAGING_TYPE=kafka -e KAFKA_TOPIC=output -e KAFKA_ADDRESS=test-kafka:9092 -e OUTPUT_WRITER_PORT=8080 agogosml/output_writer:latest


Agogosml Library


* Free software: MIT license
* Documentation: https://agogosml.readthedocs.io.

