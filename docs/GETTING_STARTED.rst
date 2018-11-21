Getting Started
===============

This solution consists of three projects:

-  `Framework`_ - The agogosml library SDK which consists of the data
   pipeline, input reader, output writer, streaming clients, etc.
-  `CLI`_: A CLI tool to help you set up a new project.
-  `Sample App`_: A sample app that represent the customer app/model

Before starting, please review agogosml `design`_

Prerequisites
-------------

-  Make sure to run bash (Linux/MacOS) or `WSL`_
-  Install `azure-cli`_
-  `Python 3.7`_
-  `Terraform`_ to provision Azure resources such as AKS and EventHub
-  `Docker`_

Setup up Development environment
--------------------------------

1. Install the CLI ``$ pip install agogosml``

2. Init the project ``$ agogosml init <folder name>``

3. Generate the code for the project. ``$ agogosml generate``. The
   generated folder structure is described `here`_ and consist with the
   input, sample and output app as well as the Azure DevOps pipelines
   for CI/CD.

.. _app/model-integration-with-agogosml:

App/Model Integration with Agogosml
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integrate your model in Agogosml by implementing a small HTTP service
that accepts POST requests and can send the HTTP POST request to
agogosml output writer. You can find an example
`here <https://github.com/Microsoft/agogosml/tree/master/sample_app>`__.

Build and test your app
~~~~~~~~~~~~~~~~~~~~~~~

In order to test your app integration with the agogosml components aka
Input/Output, you can build Docker containers with the following
`instructions`_

Provision Azure Resources
-------------------------

1. Create `Azure DevOps`_ account
2. Create `Azure Kubernetes Service`_
3. Create `Azure Event Hub`_

.. _Framework: https://github.com/Microsoft/agogosml/tree/master/agogosml
.. _CLI: https://github.com/Microsoft/agogosml/tree/master/agogosml_cli
.. _Sample App: https://github.com/Microsoft/agogosml/tree/master/sample_app
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