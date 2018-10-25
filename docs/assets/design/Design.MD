# CI/CD and Data pipeline design

## Overview

![architecure diagram](./ASB-cicd-pipeline.png)

## Requirements

- The Azure DevOps pipeline is executes the following:
  - Clone the latest (or specific) branches of a Github repository.
  - Build the repo.
  - Run linting and unit tests.
  - Execute E2E/Validation tests.
  - If all the tests have passed, push the new docker images to an Azure Container Registry.
- The Sample Application container is a place holder for any customer application image. That image needs to answer to the following conditions:
  - Implement a the HTTP endpoints protocol (TBD).
  - [Optional] Return message handling statuses to the input handler to enable a retry mechanism.
- The Input/Output components handle the following areas of the data pipeline:
  - Connectivity to the different types of events sources, such as Azure EventHubs, Kafka and HTTP (for batching)
  - Retrying failed messages
  - responsible for logging / auditing

## Testing

- Testing of the complete data pipeline will run on each DevOps build pipeline to ensure the quality of the pipeline and that messages are processed properly
- Testing components are deployed (ran) on the same docker client as the Input/Output components and acts as both events producer and events consumer (such as EventHub mock)
  - communication is internal to the docker cluster and ensures sufficient performance
- The DevOps pipeline will continuously check the tests containers exit code and accordingly will decide if the new version is passed the validation

## Open issues

- Verify docker client can be run locally on a agent VM
- Verify Kafka/EH producers/consumers mocks are available