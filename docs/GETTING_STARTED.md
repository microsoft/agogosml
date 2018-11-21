# Getting Started

This solution consists of three projects:

- [Framework](https://github.com/Microsoft/agogosml/tree/master/agogosml) - The agogosml library SDK which consists of the data pipeline, input reader, output writer, streaming clients, etc.
- [CLI](https://github.com/Microsoft/agogosml/tree/master/agogosml_cli): A CLI tool to help you set up a new project.
- [Sample App](https://github.com/Microsoft/agogosml/tree/master/sample_app): A sample app that represent the customer app/model

Before starting, please review agogosml [design](https://github.com/Microsoft/agogosml/tree/master/docs/DESIGN.md)

## Prerequisites

- Make sure to run bash (Linux/MacOS) or [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
- Install [azure-cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Python 3.7](https://www.python.org/downloads/release/python-371/)
- [Terraform](https://www.terraform.io/) to provision Azure resources such as AKS and EventHub
- [Docker](https://docs.docker.com/)

## Setup up Development environment

1. Install the CLI `$ pip install agogosml`

2. Init the project `$ agogosml init <folder name>`

3. Generate the code for the project. `$ agogosml generate`. The generated folder structure is described [here](https://github.com/Microsoft/agogosml/blob/master/agogosml_cli/README.rst#agogosml-cli-usage) and consist with the input, sample and output app as well as the Azure DevOps pipelines for CI/CD.

### App/Model Integration with Agogosml

Integrate your model in Agogosml by implementing a small HTTP service that accepts POST requests and can send the HTTP POST request to agogosml output writer. You can find an example [here](https://github.com/Microsoft/agogosml/tree/master/sample_app).

### Build and test your app

In order to test your app integration with the agogosml components aka Input/Output, you can build Docker containers with the following [instructions](https://github.com/Microsoft/agogosml/blob/master/agogosml/README.rst#overview)

## Provision Azure Resources

1. Create [Azure DevOps](https://azure.microsoft.com/en-us/services/devops/) account
2. Create [Azure Kubernetes Service](https://github.com/Microsoft/agogosml/tree/master/deployment/aks)
3. Create [Azure Event Hub](https://github.com/Microsoft/agogosml/tree/master/deployment/eventhub)