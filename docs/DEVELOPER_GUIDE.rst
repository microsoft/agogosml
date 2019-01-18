Developer Guide
===============

We love pull requests from everyone. By participating in this project,
you agree to abide by the `Microsoft Open Source Code of
Conduct <https://opensource.microsoft.com/codeofconduct/>`__




Setting up the Agogosml Library for Development
-----------------------------------------------

Requirements to Run Locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Make sure to run bash (Linux/MacOS) or `WSL`_
-  Install `azure-cli`_
-  `Python 3.7`_
-  `Terraform`_ to provision Azure resources such as AKS and EventHub
-  `Docker`_

Build with Docker and Test Your App
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Build the base image using:

.. code:: bash

    docker build -t agogosml -f agogosml/Dockerfile.agogosml agogosml

Then the input reader image:

.. code:: bash

    docker build -t agogosml/input_reader -f input_reader/Dockerfile.input_reader input_reader/


The app (replacing 'app' with your custom application name):

.. code:: bash

    docker build -t agogosml/app -f sample_app/Dockerfile.app app/

And finally the output writer:

.. code:: bash

    docker build -t agogosml/output_writer -f output_writer/Dockerfile.output_writer output_writer/



Run with Docker Locally
~~~~~~~~~~~~~~~~~~~~~~~

If you are building this locally add the following to each of the above commands:

.. code:: bash

  --build-arg CONTAINER_REG=agogosml/

Set required environment variables (You can see an example `env.example.sh <../env.example.sh>`__)

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


Setting up the CLI for Development
----------------------------------

agogosml_cli is a cli tool developed with Python using the `Click\_ <https://click.palletsprojects.com/en/7.x/>`__ in combination with `cookiecutter <https://github.com/audreyr/cookiecutter>`__. 

Requirements to Run Locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Install `pipenv <https://pipenv.readthedocs.io/en/latest/>`__ 
- `Python 3.7`_

Local Installation
~~~~~~~~~~~~~~~~~~

Installing Dependencies (and Dev Dependencies):

.. code:: bash

    $ cd agogosml_cli/
    $ pipenv install --dev
    $ pipenv run make installedit

Running Tests:

.. code:: bash

    $ pipenv run make test

Running Linter:

.. code:: bash

    $ pipenv run make lint


Test the CLI and see generated output

.. code:: bash

    $ pipenv shell

    # Create a directory for your project
    $ mkdir hello-agogosml && cd hello-agogosml

    # Init the project
    agogosml init

    # Fill in the manifest.json (Docker Container Registry, Azure Subscription, etc).
    vi manifest.json

    # Generate the code for the projects
    agogosml generate



Deployment and Provisionning to Azure
--------------------------------------

You can follow the same steps in the `User Guide <USER_GUIDE.rst#deployment-and-provisionning-to-azure>`__ to deploy the build to Azure.

Before Submitting a PR to the Project
-------------------------------------

Make sure the tests pass

Make your change. Add tests for your change. Make the tests pass

Push to your fork and `submit a pull
request <https://github.com/Microsoft/agogosml/pulls>`__.


At this point you’re waiting on us. We like to at least comment on pull
requests within three business days (and, typically, one business day).
We may suggest some changes or improvements or alternatives.

Some things that will increase the chance that your pull request is
accepted:

-  Write tests.
-  Follow our `engineering
   playbook <https://github.com/Microsoft/code-with-engineering-playbook>`__
-  Write a `good commit
   message <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`__.


.. _Framework: https://github.com/Microsoft/agogosml/tree/master/agogosml
.. _CLI: https://github.com/Microsoft/agogosml/tree/master/agogosml_cli
.. _App: https://github.com/Microsoft/agogosml/tree/master/sample_app
.. _design: https://github.com/Microsoft/agogosml/blob/master/docs/DESIGN.rst
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
