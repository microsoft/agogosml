# CLI and Scaffolding Tools Documentation

## Overview

The CLI and Scaffolding tools (agogosml-cli) was developed to help the Data Engineer scaffold a project using agogosml and to generate sample code, dependencies and configuration files. Agogosml-cli will provide commands to update the dependencies of the generated scaffold to the latest agogosml version to help the Data Engineer keep their project up to date.

## Agogosml CLI Usage

```bash
$ agogosml command [OPTIONS]
```

![CLI User Usage Flow](assets/cli/cli-user-usage-flow.png)

The Data Engineer installs the agogosml-cli and runs `agogosml init` to generate a manifest.json file. The data engineer will then modify the manifest.json and add their configuration files. The data engineer runs `agogosml generate` to generate the agogosml project.

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

agogosml-cli is a cli tool developed with Python using the [Click_](https://click.palletsprojects.com/en/7.x/) in combination with [cookiecutter](https://github.com/audreyr/cookiecutter).
