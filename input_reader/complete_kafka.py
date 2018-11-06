import os
import time
from kafka_client_broker import KafkaClientBroker
from pykafka.exceptions import InvalidTopic, NoBrokersAvailableError

retries = 5
while retries != 0:
    time.sleep(2)
    try: 
        hosts = f'{os.environ["KAFKA_HOST"]}:{os.environ["KAFKA_PORT"]}'
        client = KafkaClientBroker(hosts)
        client.create_topic(os.environ["KAFKA_TOPIC"])

        consumer = topic.get_simple_consumer(use_rdkafka=True)

        print("SUCCESS")
    except (InvalidTopic, NoBrokersAvailableError) as e:
        retries -= 1
