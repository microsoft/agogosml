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
app (that holds a trained ML model) and an output writer. The three
components are instrumented using one Docker container per component.


Input Reader
________________
The input reader acts as the data receiver and obtains the data required as
input for the ML model. The package supports both Kafka and EventHub.


Output Writer
_____________
The output writer receives the scored data from the app and sends it onto
a streaming client (a Kafka or Eventhub instance).


App
_____________
The app receives data from the input reader and feeds it to the ML model
for scoring. Once scored the data is sent onto the output writer.


Build with Docker
_________________________

Install `Docker <https://docs.docker.com/install/>`_ .

Build the base image using:

.. code:: bash

    $ docker build -t agogosml/agogosml -f agogosml/Dockerfile.agogosml agogosml

Then the input reader image:

.. code:: bash

    $ docker build -t agogosml/input_reader -f input_reader/Dockerfile.input_reader .


The app:

.. code:: bash

    $ docker build -t agogosml/app -f sample_app/Dockerfile.app .

And finally the output writer:

.. code:: bash

    $ docker build -t agogosml/output_writer -f output_writer/Dockerfile.output_writer .



Run with Docker
_________________________

Set required environment variables

.. code:: bash

    $ export INPUT_READER_NAME=input-reader
    $ export APP_NAME=app
    $ export OUTPUT_WRITER_NAME=output-writer
    $ export NETWORK_NAME=testnetwork       # Docker network name
    $ export MESSAGING_TYPE=eventhub        # eventhub/kafka
    $ export AZURE_STORAGE_ACCOUNT=         # storage account name for EH processor
    $ export AZURE_STORAGE_ACCESS_KEY=      # storage account key for EH processor
    $ export LEASE_CONTAINER_NAME=          # storage account container for EH processor
    $ export EVENT_HUB_NAMESPACE=           # EH namespace
    $ export INPUT_EVENT_HUB_NAME=          # input EH
    $ export INPUT_EVENT_HUB_SAS_POLICY=    # input EH policy name
    $ export INPUT_EVENT_HUB_SAS_KEY=       # input EH policy key
    $ export OUTPUT_EVENT_HUB_NAME=         # output EH
    $ export OUTPUT_EVENT_HUB_SAS_POLICY=   # output EH policy name
    $ export OUTPUT_EVENT_HUB_SAS_KEY=      # output EH policy key
    $ export APP_PORT=5000                  # app port
    $ export OUTPUT_WRITER_PORT=8080        # output writer app port


A Docker network must then be created with:

.. code:: bash

    $ docker network create $NETWORK_NAME

The four Docker images must then be run, prepending the parameter ``-e`` to any
environment variables. An example of how to run one of these Docker images is:

.. code:: bash

    # Run Input reader
    $ docker run --rm --network $NETWORK_NAME --name $INPUT_READER_NAME -d \
      -e MESSAGING_TYPE=$MESSAGING_TYPE \
      -e AZURE_STORAGE_ACCOUNT=$AZURE_STORAGE_ACCOUNT \
      -e AZURE_STORAGE_ACCESS_KEY=$AZURE_STORAGE_ACCESS_KEY \
      -e LEASE_CONTAINER_NAME=$LEASE_CONTAINER_NAME \
      -e EVENT_HUB_NAMESPACE=$EVENT_HUB_NAMESPACE \
      -e EVENT_HUB_NAME=$INPUT_EVENT_HUB_NAME \
      -e EVENT_HUB_SAS_POLICY=$INPUT_EVENT_HUB_SAS_POLICY \
      -e EVENT_HUB_SAS_KEY=$INPUT_EVENT_HUB_SAS_KEY \
      -e APP_HOST=$APP_NAME \
      -e APP_PORT=$APP_PORT \
      agogosml/input_reader:latest

    # Run app
    $ docker run --rm --name $APP_NAME -d --network $NETWORK_NAME \
      -e HOST=$APP_NAME \
      -e PORT=$APP_PORT \
      -e OUTPUT_URL=http://$OUTPUT_WRITER_NAME:$OUTPUT_WRITER_PORT \
      -e SCHEMA_FILEPATH=schema_example.json \
      agogosml/app

    # Run Output writer
    $ docker run --rm --name $OUTPUT_WRITER_NAME -d --network $NETWORK_NAME \
    -e MESSAGING_TYPE=$MESSAGING_TYPE \
    -e EVENT_HUB_NAMESPACE=$EVENT_HUB_NAMESPACE \
    -e EVENT_HUB_NAME=$OUTPUT_EVENT_HUB_NAME \
    -e EVENT_HUB_SAS_POLICY=$OUTPUT_EVENT_HUB_SAS_POLICY \
    -e EVENT_HUB_SAS_KEY=$OUTPUT_EVENT_HUB_SAS_KEY \
    -e OUTPUT_WRITER_HOST=$OUTPUT_WRITER_NAME \
    -e OUTPUT_WRITER_PORT=$OUTPUT_WRITER_PORT \
    agogosml/output_writer:latest

Now you can send a message to Event Hub with the following sample payload and check the output Event Hub for the transformed result:

.. code:: bash

    {
	    "key": "SAMPLE_KEY",
        "intValue": 40
    }



Agogosml Library


* Free software: MIT license
* Documentation: https://agogosml.readthedocs.io.

