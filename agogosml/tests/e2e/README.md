# Running the tests - Instructions

1. create .env and .env.app files for the input/output components and the sample app respectively.
2. run

```bash
docker-compose up --scale input-reader=2 -d
```

this will launch all the containers.

3. issue a GET command to localhost:2000/send
this will generate first events in the EH that will be picked up by the input-reader

4. issue a GET command to localhost:2000/receive, a valid response is a non empty one