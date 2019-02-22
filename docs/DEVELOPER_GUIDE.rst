Developer Guide
===============

This guide is for those that wish to develop on Agogosml. 
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
-  `Docker`_
-  Optional: `Terraform`_ to provision Azure resources such as AKS and EventHub

Project Structure
~~~~~~~~~~~~~~~~~

In ``agogosml_cli/`` is all code related to the CLI, i.e. generating the pipeline project locally for a user. 
``agogosml/agogosml_cli/cli/templates/{{cookiecutter.PROJECT_NAME_SLUG}}/`` contains the structure that is generated. 
The ``templates/apps/`` folder has the two sample applications, one of which will be selected to create the pipeline with.

The pipeline generated simply uses a base image of Agogosml available in PyPi. You can use the commands in `dockerbuild.sh` to build
the input, output, and application Docker containers. If changes are made within this CLI implementation, to test you can simply run 
the end-to-end tests, using the docker-compose files we provide. These compose files spin up all three images, and send test messages
from another ``testgen`` container that is built in the compose.  

In the CLI we also have infrastructure deployment, Helm charts for Kubernetes orchestration, and end-to-end tests.

The code for Agogosml lives in ``agogosml/agogosml/``. To test the pipeline with your local version, simply
build ``agogosml/Dockerfile.agogosml`` as your base image before building the input, output, and app containers. The 
instructions are in the below section.

To test locally, create a virtual environment within agogosml and install the package.

.. code:: bash

    cd agogosml/agogosml
    python3 -m venv venv
    . venv/bin/activate
    cd ..
    pip install -e agogosml/

The final step installs agogosml as if it were a remote package. This way you can locally
test changes immediately.

Build the Pipeline with Docker using your Local Version of Agogosml
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From the top level directory, build the base image using. You can add a --build-arg CONTAINER_REG=
to any of these commands, but unsure to tag your base image with the CONTAINER_REG/. 

.. code:: bash

    docker build -t agogosml -f agogosml/Dockerfile.agogosml agogosml

Now navigate to the CLI at ``agogosml/agogosml_cli/cli/templates/{{cookiecutter.PROJECT_NAME_SLUG}}/``
Build the input reader and output writer image: 

.. code:: bash

    docker build -t agogosml/input_reader -f input_reader/Dockerfile.input_reader input_reader/
    docker build -t agogosml/output_writer -f output_writer/Dockerfile.output_writer output_writer/


Now navigate to the CLI at ``agogosml/agogosml_cli/cli/templates/{{cookiecutter.PROJECT_NAME_SLUG}}/``
Build the custom application:

.. code:: bash

    docker build -t agogosml/{{cookiecutter.PROJECT_NAME_SLUG}} -f {{cookiecutter.PROJECT_NAME_SLUG}}/Dockerfile.{{cookiecutter.PROJECT_NAME_SLUG}} {{cookiecutter.PROJECT_NAME_SLUG}}/


Run with Docker Locally
~~~~~~~~~~~~~~~~~~~~~~~

Set required environment variables in the PATH (You can see an example `env.example.sh <../env.example.sh>`__)

Below are the required variables to run the ``docker-compose-agogosml.yml`` file locally. We hardcode
some of the enviromment variables there, so if you want to run each container separately, please refer
to ``env.example.sh``.

.. code:: bash

    export MESSAGING_TYPE=eventhub        # eventhub/kafka

    # Event Hub Specific Variables 

    export MESSAGING_TYPE=                          # eventhub/kafka
    export CONTAINER_REG=                           # this can be empty for local dev.
    export TAG=                                     # latest

    # Fill out if using Event Hubs as messaging service.
    export EVENT_HUB_NAMESPACE=
    export EVENT_HUB_NAME_INPUT=                    # Event Hub to receive incoming messages
    export EVENT_HUB_NAME_OUTPUT=                   # Event Hub to receive outgoing messages
    export EVENT_HUB_SAS_POLICY=                    # SAS Policy created for both input and output
    export EVENT_HUB_SAS_KEY_INPUT=                 # Key for input event hub SAS policy
    export EVENT_HUB_SAS_KEY_OUTPUT=                # Key for output event hub SAS policy

    export AZURE_STORAGE_ACCOUNT=                   # Storage account for Event Hub
    export AZURE_STORAGE_ACCESS_KEY=
    export LEASE_CONTAINER_NAME_INPUT=              # Container for input events
    export LEASE_CONTAINER_NAME_OUTPUT=             # Container for output events
    export EVENT_HUB_CONSUMER_GROUP=                # Default is $default

    # Fill out if using Kafka as messaging service, including Kafka with Event Hubs Integration
    export KAFKA_ADDRESS=
    export KAFKA_TIMEOUT=
    export KAFKA_TOPIC_INPUT=
    export KAFKA_TOPIC_OUTPUT=
    export KAFKA_CONSUMER_GROUP=

    # Fill out the following if using Kafka Enabled Event Hubs Only. See instruction https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-create-kafka-enabled.
    # Ensure that EVENTHUB_KAFKA_CONNECTION_STRING is NOT set if you are using pure Kafka.

    export EVENTHUB_KAFKA_CONNECTION_STRING=        # Connection string-primary key in the Event Hub

    # Local SSL Certificate - only necessary to define path to local cert if you are running locally. i.e. something like /usr/local/etc/openssl/cert.pem
    
    export SSL_CERT_LOCATION=

    # Application Insights telemetry
    export APPINSIGHTS_INSTRUMENTATIONKEY=
    export APPINSIGHTS_ENDPOINT= # Only needed if using on-premises telemetry

Setting up the CLI for Development
----------------------------------

agogosml_cli is a cli tool developed with Python using the `Click\_ <https://click.palletsprojects.com/en/7.x/>`__ in combination with `cookiecutter <https://github.com/audreyr/cookiecutter>`__. 

Requirements to Run Locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `Python 3.7`_

Local Installation
~~~~~~~~~~~~~~~~~~

Installing Dependencies (and Dev Dependencies):

.. code:: bash

    $ cd agogosml_cli/
    $ python3 -m venv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt
    $ pip install -r requirements-dev.txt
    $ make installedit

Running Tests:

.. code:: bash

    $ make test

Running Linter:

.. code:: bash

    $ make lint


Test the CLI and see generated output

.. code:: bash

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
