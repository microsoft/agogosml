#!/usr/bin/env bash

docker build --no-cache -t agogosml -f agogosml/Dockerfile.agogosml agogosml/
docker build --no-cache -t input_reader -f input_reader/Dockerfile.input_reader input_reader/
docker build --no-cache -t output_writer -f output_writer/Dockerfile.output_writer output_writer/
docker build --no-cache -t sample_app -f {{cookiecutter.PROJECT_NAME_SLUG}}/Dockerfile.{{cookiecutter.PROJECT_NAME_SLUG}} {{cookiecutter.PROJECT_NAME_SLUG}}/
