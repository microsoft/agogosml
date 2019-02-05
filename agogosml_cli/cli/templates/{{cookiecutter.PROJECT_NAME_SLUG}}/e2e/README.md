### Running the End to End Test

1. You can use the generated Azure DevOps Pipeline (`e2e-pipeline.json`) and import it to your Azure DevOps Pipeline.
2. Set all the correct environment variables
3. Queue the pipeline for build.

### Alternative: Running the End to End Test Locally

The following are instructions to run the end to end test locally. Even though you are running the tests
locally, they are still an end to end test and depend on deployed Azure resources.

1. Make sure to set the following environment variables so that they may be correctly read by Docker Compose.

```bash
    EVENT_HUB_NAMESPACE=
    EVENT_HUB_NAME=
    EVENT_HUB_SAS_POLICY=
    EVENT_HUB_SAS_KEY_INPUT=
    EVENT_HUB_NAME_INPUT=
    EVENT_HUB_SAS_KEY_OUTPUT=
    EVENT_HUB_NAME_OUTPUT=
    AZURE_STORAGE_ACCOUNT=
    AZURE_STORAGE_ACCESS_KEY=
    LEASE_CONTAINER_NAME_OUTPUT=
    LEASE_CONTAINER_NAME_INPUT=
    AZURE_STORAGE_ACCESS_KEY=
    AZURE_STORAGE_ACCOUNT=
    EVENT_HUB_CONSUMER_GROUP=
    MESSAGING_TYPE=
    CONTAINER_REG=
    TAG=
    APP_TAG=
```

2. Run Docker Compose

```bash
docker-compose -f docker-compose-agogosml.yml up --scale input-reader=2 -d
```

This will launch all the containers required for the end to end test.

3. In order to execute the e-2-e test, a test generator app is required.
   You can use the included testgen app `docker-compose-testgen.yml` to execute the test.

Note: You have to run `docker-compose-agogosml.yml` before running `docker-compose-testgen.yml`

```bash
docker-compose -f docker-compose-testgen.yml up
```

The testgen app will generate and send events to EventHub or Kafka that will be picked up by the input-reader and start the pipeline.
At the end of the process the testgen app will also read the results sent to EventHub and print them for you to validate the process.

The pipeline can also be run fully locally by using a containerized Kafka instance via:

```bash
docker-compose -f docker-compose-agogosml.yml -f docker-compose-agogosml.local.yml up
```
