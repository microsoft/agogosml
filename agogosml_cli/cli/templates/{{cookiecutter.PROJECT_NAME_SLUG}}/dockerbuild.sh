#!/usr/bin/env bash

docker build -t agogosml -f agogosml/Dockerfile.agogosml agogosml/
docker build -t input_reader -f input_reader/Dockerfile.input_reader input_reader/
docker build -t output_writer -f output_writer/Dockerfile.output_writer output_writer/
docker build -t {{cookiecutter.PROJECT_NAME_SLUG}} -f {{cookiecutter.PROJECT_NAME_SLUG}}/Dockerfile.{{cookiecutter.PROJECT_NAME_SLUG}} {{cookiecutter.PROJECT_NAME_SLUG}}/
