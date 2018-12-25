# Running the tests - Instructions

1. Create .env and .env.app files for the input/output components and the sample app respectively.
2. run

```bash
docker-compose up --scale input-reader=2 -d
```

this will launch all the containers required for the end to end test.

3. In order to execute the e-2-e test, a test generator app is required.
You can use the included testgen app `docker-compose.yml` to execute the test.

The test will generate and send events to EventHub that will be picked up by the input-reader and start the pipeline.
At the end of the process the testgen app will also read the results sent to EventHub and print them for you to validate the process.
