# CLI and Scaffolding Tools Documentation

## Overview

The CLI and Scaffolding tools (agogosml-cli) was developed to help the Data Engineer scaffold a project using agogosml and to generate sample code, dependencies and configuration files. Agogosml-cli will provide commands to update the dependencies of the generated scaffold to the latest agogosml version to help the Data Engineer keep their project up to date.

## Agogosml CLI Usage

```bash
$ agogosml command [OPTIONS]
```

![CLI User Usage Flow](../docs/assets/cli/cli-user-usage-flow.png)

The Data Engineer installs the agogosml-cli and runs `agogosml init` to generate a manifest.json file. The data engineer will then modify the manifest.json and add their configuration files. The data engineer runs `agogosml generate` to generate the agogosml project. The generated scaffold will include the following files:

* `.env` - This file will be read by the Pipfile and contains an initial array of keys= for you to fill out.
* `manifest.json` - This file is the configuration file for agogosml-cli.
* `cicd-pipeline.yml` - This yaml file will contain the Azure DevOps ci/cd pipeline for an agogosml project.
* `data-pipeline.yml` - This yaml file will contain the Azure DevOps data pipeline for an agogosml project.
* `Pipfile` - This file is the pipenv file used to configure the included sample app. It may also contain runs scripts to simplify deployment (coming soon.)
* `sample_app/` - This a simple data transformation app that shows you how to read from the InputReader and write to the OutputWriter data pipeline components.
* `tests/e2e/` - This a directory containing end to end integration tests for your deployed data pipeline.
* `tests/validation` - This a directory containing various useful validation tests.

### Install

Coming soon.

### CLI Commands

#### init - Creates a manifest.json file

```bash
$ agogosml init [--force|-f] <name>
```

`agogosml init <name>` will generate a manifest file that contains all the configuration variables for an agogosml project. `<name>` is the name you would like to give your agogosml project.

#### generate - Generates an agogosml project

```bash
$ agogosml generate
$ agogosml generate <folder>
$ agogosml generate [--config|-c]
$ agogosml generate [--config|-c] <folder>

alias: agogosml g
```

`agogosml generate` will generate a scaffold of an agogosml project based on a manifest file if found in the current or target folder or as specified by `--config`.

#### update - Updates an agogosml project

```bash
$ agogosml update
$ agogosml update <folder>
```

`agogosml update` will update a scaffolded agogosml project. It will update the agogosml dependencies to the latest version.

## How To Contribute

agogosml-cli is a cli tool developed with Python using the [Click_](https://click.palletsprojects.com/en/7.x/) in combination with [cookiecutter](https://github.com/audreyr/cookiecutter). The cli uses [pipenv](https://pipenv.readthedocs.io/en/latest/) for dependencies management.

### How To Setup Dev Environment

Clone the git repository, cd into the cli folder,

```bash
git clone https://github.com/Microsoft/agogosml
cd agogosml/agogosml-cli/
pipenv install
```

### How to Run Tests

### How to Add a Command to the CLI

### How to Package and Install the CLI for Local Development & Testing

