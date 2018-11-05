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
    messages = kafka_broker.receive()
    for message in messages:
        requests.post("http://localhost:5000/input", data=message)
