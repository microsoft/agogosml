User Guide - Getting Started
============================

Before starting, please review agogosml `design`_

Prerequisites
-------------

-  Make sure to run bash (Linux/MacOS) or `WSL`_
-  Install `azure-cli`_
-  `Python 3.7`_
-  `Terraform`_ to provision Azure resources such as AKS and EventHub
-  `Docker`_

Create a New Project
--------------------------------

.. code-block:: bash
    # 1. Installing the CLI
    pip install agogosml_cli

    # 2. Create a directory for your project
    mkdir hello-agogomsl
    cd hello-agogomsl

    # 3. Init the project
    agogosml init

    # 4. Fill in the manifest.json (Docker Container Registry, Azure Subscription, etc).
    vi manifest.json

    # 5. Generate the code for the projects
    agogosml generate


The generated folder structure consists of the input reader, customer app and output writer as well as the Azure DevOps pipelines for CI/CD.

.. _app/model-integration-with-agogosml:

App/Model Integration with Agogosml
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integrate your model in Agogosml by implementing a small HTTP service
that accepts POST requests and can send the HTTP POST request to
agogosml output writer. You can find an example
`here <https://github.com/Microsoft/agogosml/tree/master/sample_app>`__.

Build with Docker and Test Your App
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install `Docker <https://docs.docker.com/install/>`_ .

Build the base image using:

.. code:: bash

    docker build -t agogosml/agogosml -f agogosml/Dockerfile.agogosml agogosml

Then the input reader image:

.. code:: bash

    docker build -t agogosml/input_reader -f input_reader/Dockerfile.input_reader .


The app:

.. code:: bash

    docker build -t agogosml/app -f sample_app/Dockerfile.app .

And finally the output writer:

.. code:: bash

    docker build -t agogosml/output_writer -f output_writer/Dockerfile.output_writer .

Run with Docker Locally
~~~~~~~~~~~~~~~~~~~~~~~

Set required environment variables

.. code:: bash

    export INPUT_READER_NAME=input-reader
    export APP_NAME=app
    export OUTPUT_WRITER_NAME=output-writer
    export NETWORK_NAME=testnetwork       # Docker network name
    export MESSAGING_TYPE=eventhub        # eventhub/kafka
    export AZURE_STORAGE_ACCOUNT=         # storage account name for EH processor
    export AZURE_STORAGE_ACCESS_KEY=      # storage account key for EH processor
    export LEASE_CONTAINER_NAME=          # storage account container for EH processor
    export EVENT_HUB_NAMESPACE=           # EH namespace
    export INPUT_EVENT_HUB_NAME=          # input EH
    export INPUT_EVENT_HUB_SAS_POLICY=    # input EH policy name
    export INPUT_EVENT_HUB_SAS_KEY=       # input EH policy key
    export OUTPUT_EVENT_HUB_NAME=         # output EH
    export OUTPUT_EVENT_HUB_SAS_POLICY=   # output EH policy name
    export OUTPUT_EVENT_HUB_SAS_KEY=      # output EH policy key
    export APP_PORT=5000                  # app port
    export OUTPUT_WRITER_PORT=8080        # output writer app port


A Docker network must then be created with:

.. code:: bash

    docker network create $NETWORK_NAME

The four Docker images must then be run, prepending the parameter ``-e`` to any
environment variables. An example of how to run one of these Docker images is:

.. code:: bash

    # Run Input reader
    docker run --rm --network $NETWORK_NAME --name $INPUT_READER_NAME -d \
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
    docker run --rm --name $APP_NAME -d --network $NETWORK_NAME \
        -e HOST=$APP_NAME \
        -e PORT=$APP_PORT \
        -e OUTPUT_URL=http://$OUTPUT_WRITER_NAME:$OUTPUT_WRITER_PORT \
        -e SCHEMA_FILEPATH=schema_example.json \
        agogosml/app

    # Run Output writer
    docker run --rm --name $OUTPUT_WRITER_NAME -d --network $NETWORK_NAME \
        -e MESSAGING_TYPE=$MESSAGING_TYPE \
        -e EVENT_HUB_NAMESPACE=$EVENT_HUB_NAMESPACE \
        -e EVENT_HUB_NAME=$OUTPUT_EVENT_HUB_NAME \
        -e EVENT_HUB_SAS_POLICY=$OUTPUT_EVENT_HUB_SAS_POLICY \
        -e EVENT_HUB_SAS_KEY=$OUTPUT_EVENT_HUB_SAS_KEY \
        -e OUTPUT_WRITER_HOST=$OUTPUT_WRITER_NAME \
        -e OUTPUT_WRITER_PORT=$OUTPUT_WRITER_PORT \
        agogosml/output_writer:latest

Now you can send a message to Event Hub with the following sample payload and check the output Event Hub for the transformed result:

.. code:: json

    {
	    "key": "SAMPLE_KEY",
        "intValue": 40
    }

Deployment and Provisionning to Azure
--------------------------------------

1. Create `Azure DevOps`_ account
2. Create `Azure Kubernetes Service`_
3. Create `Azure Event Hub`_

.. _Framework: https://github.com/Microsoft/agogosml/tree/master/agogosml
.. _CLI: https://github.com/Microsoft/agogosml/tree/master/agogosml_cli
.. _App: https://github.com/Microsoft/agogosml/tree/master/sample_app
.. _design: https://github.com/Microsoft/agogosml/tree/master/docs/DESIGN.md
.. _WSL: https://docs.microsoft.com/en-us/windows/wsl/install-win10
.. _azure-cli: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
.. _Python 3.7: https://www.python.org/downloads/release/python-371/
.. _Terraform: https://www.terraform.io/
.. _Docker: https://docs.docker.com/
.. _here: https://github.com/Microsoft/agogosml/blob/master/agogosml_cli/README.rst#agogosml-cli-usage
.. _instructions: https://github.com/Microsoft/agogosml/blob/master/agogosml/README.rst#overview
.. _Azure DevOps: https://azure.microsoft.com/en-us/services/devops/
.. _Azure Kubernetes Service: https://github.com/Microsoft/agogosml/tree/master/deployment/aks
.. _Azure Event Hub: https://github.com/Microsoft/agogosml/tree/master/deployment/eventhub


CLI and Scaffolding Tools
=========================

Overview
--------

The CLI and Scaffolding tools (agogosml_cli) was developed to help the
Data Engineer scaffold a project using agogosml and to generate sample
code, dependencies and configuration files. agogosml_cli will provide
commands to update the dependencies of the generated scaffold to the
latest agogosml version to help the Data Engineer keep their project up
to date.

Agogosml CLI Usage
------------------

.. code:: bash

   agogosml command [OPTIONS]

.. figure:: ./_static/cli-user-usage-flow.png
   :alt: CLI User Usage Flow

   CLI User Usage Flow

The Data Engineer installs the agogosml_cli and runs ``agogosml init``
to generate a manifest.json file. The data engineer will then modify the
manifest.json and add their configuration files. The data engineer runs
``agogosml generate`` to generate the agogosml project. The generated
scaffold will include the following files:

-  ``.env`` - This file will be read by the Pipfile and contains an
   initial array of keys= for you to fill out.
-  ``manifest.json`` - This file is the configuration file for
   agogosml_cli.
-  ``cicd-pipeline.yml`` - This yaml file will contain the Azure DevOps
   ci/cd pipeline for an agogosml project.
-  ``data-pipeline.yml`` - This yaml file will contain the Azure DevOps
   data pipeline for an agogosml project.
-  ``Pipfile`` - This file is the pipenv file used to configure the
   included app. It may also contain runs scripts to simplify
   deployment (coming soon).
-  ``sample_app/`` - This a simple data transformation app that shows
   you how to read from the InputReader and write to the OutputWriter
   data pipeline components.
-  ``tests/e2e/`` - This a directory containing end to end integration
   tests for your deployed data pipeline.
-  ``tests/validation`` - This a directory containing various useful
   validation tests.

Install
~~~~~~~

Coming soon.

CLI Commands
~~~~~~~~~~~~

init - Creates a manifest.json file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   agogosml init [--force|-f] <folder>

``agogosml init <folder>`` will generate a manifest file that contains
all the configuration variables for an agogosml project. ``<folder>`` is
the folder you would like to give use for your agogosml project.

generate - Generates an agogosml project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   agogosml generate
   agogosml generate <folder>
   agogosml generate [--config|-c]
   agogosml generate [--config|-c] <folder>

   alias: agogosml g

``agogosml generate`` will generate a scaffold of an agogosml project
based on a manifest file if found in the current or target folder or as
specified by ``--config``.

update - Updates an agogosml project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   agogosml update
   agogosml update <folder>

``agogosml update`` will update a scaffolded agogosml project. It will
update the agogosml dependencies to the latest version.

