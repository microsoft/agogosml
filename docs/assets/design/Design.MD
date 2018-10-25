# CI/CD and Data pipeline design

## Overview

![architecure diagram](./ASB-cicd-pipeline.png)

This Azure DevOps pipeline is responsible to get the latest (or specified) branchs of Github code, clone, build run unit tests, linting tests, E2E tests and finally if all tests passed, push the new docker images to a container registry

## Requirements

- The customer's application is a place holder for any application image. The only requirement is to implement the HTTP endpoints protocol (TBD)
- The Input/Output components are responsible to handle the connectivity to the different events hubs, instead of the app itself:
  - responsible for the interaction with different events sources such as Azure EventHubs, Kafka and HTTP (for batching)
  - responsible for retrying failed messages
- Logging and auditing libraries will be created to be used across all images
- The retry mechanism is optional and is configurable
  - if enabled, a message processed confirmation is required

## Testing

- Testing of the complete data pipeline will run on each DevOps build pipeline to ensure the quality of the pipeline and that messages are processed properly
- Testing components are deployed (ran) on the same docker client as the Input/Output components and acts as both events producer and events consumer (such as EventHub mock)
  - communication is internal to the docker cluster and ensures sufficient performance
- The DevOps pipeline will continuously check the tests containers exit code and accordingly will decide if the new version is passed the validation

## Open issues

- Verify docker client can be run locally on a agent VM
- Verify Kafka/EH producers/consumers mocks are available