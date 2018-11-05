from kafka_client_broker import KafkaClientBroker
import json
import datetime

config = {
    'bootstrap.servers': '127.0.0.1:9092',
    'group.id': 'group2',
    'enable.auto.commit': False
}

topic = 'testing'

if __name__ == '__main__':
    kafka_broker = KafkaClientBroker(config)
    if not kafka_broker.topic_exists(topic):
        kafka_broker.create_topic(topic, max_partitions=5)
    for _ in range(10000):
        example_message = {
            "intValue": 50,
            "floatValue": 3.7,
            "stringValue": "Hello!",
            "boolValue": True,
            "timeValue": datetime.datetime.now()
        }
        serialized_message = json.dumps(example_message)
        kafka_broker.send(serialized_message)
