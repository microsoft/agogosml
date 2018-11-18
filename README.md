# agogosml

# Quick Links

- [Intro](#intro)
- [Getting Started](#getting-started)
- [Contributing](./CONTRIBUTING.rst)
- [License](./LICENSE)
- [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/)
- [Backlog](https://waffle.io/Microsoft/agogosml)
- [Design and Architecture](./docs/assets/design/README.md)

# Intro

agogosml is a data processing pipeline project that addresses the common need for operationalizing ML models. This covers the complete workflow of training, deploying, scoring and monitoring the models in production at scale. The key focus will be on production ready re-training and scoring. The taken approach will be agnostic to the data science workflow of building the models, but the initial project will be scoped towards traditional ML techniques (non deep-learning) but might be extended when required/requested through additional customer engagements.

# Getting Started

## Prerequisites

- Make sure to run on bash or [Windows Bash](https://www.windowscentral.com/how-install-bash-shell-command-line-windows-10)
- [Create an SSH key on bash](https://docs.joyent.com/public-cloud/getting-started/ssh-keys/generating-an-ssh-key-manually/manually-generating-your-ssh-key-in-windows)
- Install [azure-cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Maven 3.0](https://maven.apache.org/download.cgi) or higher
- [Python 3.7](https://www.python.org/downloads/release/python-371/) 
- Run `make requirements` - Install Python requirements Python packages.

## Projects

This solution consists of two projects;
- [agogosml](./agogosml): The agogosml library sdk which consists of the data pipeline, input reader, output writer, streaming clients, etc. 
- [agogosml_cli](./agogosml_cli): A cli meant to help you set up a new project via cli

## Installing prerequisites

```
If you’re on MacOS, you can install Pipenv easily with Homebrew:

$ brew install pipenv
Or, if you’re using Fedora 28:

$ sudo dnf install pipenv
```

## Setting up Development environment

```
git clone https://github.com/Microsoft/agogosml
cd agogosml
```

## Deploymet to Azure

- [Deploy resources to Azure AKS using Terraform](./deployment/aks)
- [Deploy application using k8s helm chart](./deployment/helm_chart)

### Running tests for agogosml project

The following bash lines will run unit tests on agogosml project locally:

```
cd agogosml
# install dependencies in the virtual environment
pipenv install && pipenv install --dev
# installs agogosml locally
pipenv run python setup.py install
# run the tests
pipenv run make test
```

### Running tests for agogosml_cli project

[This should be updated]
The following bash lines will run unit tests on agogosml_cli project locally:

```
cd agogosml_cli
# install dependencies in the virtual environment
pipenv install && pipenv install --dev
# installs agogosml locally
pipenv run python setup.py install
# run the tests
pipenv run make test
```

# Additional Information

The following list should be updated and attached with links:
- GDPR
- ML Model
- CI/CD Pipeline
- Blue/Green Deployment
- Logging

# Related projects and useful resources

-  https://github.com/jakkaj/ravenswood
-  https://github.com/jakkaj/ml-train-deploy-vsts-k8s
-  https://github.com/Microsoft/presidio
-  https://github.com/timfpark/topological
-  https://github.com/lawrencegripper/ion
-  https://github.com/Azure/AI-predictivemaintenance and `this
   page <https://na01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fgithub.com%2FAzure%2FAI-PredictiveMaintenance%2Ftree%2Fmaster%2Fdocs&data=02%7C01%7C%7C0bc38fbfbe0e45b9364e08d60ecfc936%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C636712682921627767&sdata=CXvxvfzl%2FnoLlIZV7p7LBQTyzJdrL8rvwYlDxB5CsQE%3D&reserved=0>`__
   shows the modeling pipeline and the operationalized pipeline.
-  `Happy Paths – A reference
   architecture <https://microsoft.sharepoint.com/teams/CECRMSP/Shared%20with%20Microsoft/Forms/AllItems.aspx?slrid=0c878a9e%2Da0d2%2D0000%2Db062%2Dfea03d1c2137&RootFolder=%2Fteams%2FCECRMSP%2FShared%20with%20Microsoft%2FAI%20CAT%20Materials%2FCustom%20AI%20Reference%20Architectures&FolderCTID=0x012000CC11EAFABCEF3D40B8E0D96CF1BA4810>`__
-  `Case Study on fraud
   detection <https://azure.microsoft.com/en-us/blog/two-seconds-to-take-a-bite-out-of-mobile-bank-fraud-with-artificial-intelligence/>`__

