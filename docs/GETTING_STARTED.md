# Getting Started

## Create Environment Variables File

Create a `.env` file in the root of the project (Make sure line endings are LF) with the following variables:

- RESOURCE_GROUP_NAME: The resource group the resources are located in
- EVENTHUBS_NAMESPACE: The namespace of the eventhubs to create instances to
- EVENTHUBS_INSTANCES: An array of names to create, i.e.: ehinstance1;ehinstance2
- STORAGE_ACCOUNT_NAME: Storage Account name
- STORAGE_ACCOUNT_KEY: Storage Account key
- STORAGE_CONTAINERS: Storage containers to create, i.e.: container1;container2

## Load the environment variables locally

Run the following command locally to load the environment variables to your local environment:

```sh
export $(grep -v '^#' .env | xargs)
```

## Run the deployment command

```sh
./tests/scripts/deploy-test.sh build1
```

## Cleanup deployment

```sh
./tests/scripts/cleanup-test.sh build1
```