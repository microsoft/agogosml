# Copy this file to env.private.sh, and change the variables appropriately

MESSAGING_TYPE=eventhub

# port and host the custom app is running on
APP_PORT=               
APP_HOST=
# port and host the output server is running on
OUTPUT_WRITER_PORT=
OUTPUT_WRITER_HOST=

# To run the custom app
HOST=                # Same as APP_PORT 
PORT=                # Same as APP_HOST
OUTPUT_URL=
SCHEMA_FILEPATH=
MODEL_PATH=

# Event Hub Specific
AZURE_STORAGE_ACCOUNT=
AZURE_STORAGE_ACCESS_KEY=
LEASE_CONTAINER_NAME_INPUT=
LEASE_CONTAINER_NAME_OUTPUT=
EVENT_HUB_NAMESPACE=
EVENT_HUB_NAME_INPUT=
EVENT_HUB_SAS_POLICY=       # SAS Policy for Both Input and Output EH
EVENT_HUB_SAS_KEY_INPUT=
EVENT_HUB_NAME_OUTPUT=
EVENT_HUB_SAS_KEY_OUTPUT=

# Kafka or Kafka with Event Hub Specific
KAFKA_ADDRESS=
KAFKA_TIMEOUT=
KAFKA_TOPIC_INPUT=
KAFKA_TOPIC_OUTPUT=
KAFKA_CONSUMER_GROUP=

# Kafka and Event Hub Specific
EVENTHUB_KAFKA_CONNECTION_STRING=
SSL_CERT_LOCATION= # Only needed if running locally without Docker