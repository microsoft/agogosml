#!/usr/bin/env bash

docker build -t {{cookiecutter.PROJECT_NAME_SLUG}} -f {{cookiecutter.PROJECT_NAME_SLUG}}/Dockerfile.{{cookiecutter.PROJECT_NAME_SLUG}} {{cookiecutter.PROJECT_NAME_SLUG}}/
docker build -t agogosml/input_reader -f input_reader/Dockerfile.input_reader input_reader/
docker build -t agogosml/output_writer -f output_writer/Dockerfile.output_writer output_writer/
