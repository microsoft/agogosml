import os
import time
from pykafka import KafkaClient
from pykafka.exceptions import InvalidTopic, NoBrokersAvailableError

retries = 5
while retries != 0:
    time.sleep(2)
    try: 
        hosts = f'{os.environ["KAFKA_HOST"]}:{os.environ["KAFKA_PORT"]}'
        client = KafkaClient(hosts=hosts)
        topic = client.topics[os.environ["KAFKA_TOPIC"]]

        consumer = topic.get_simple_consumer(use_rdkafka=True)

        print("SUCCESS")
    except (InvalidTopic, NoBrokersAvailableError) as e:
        retries -= 1

