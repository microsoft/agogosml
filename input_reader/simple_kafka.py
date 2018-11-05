from pykafka import KafkaClient

client = KafkaClient(hosts="http://localhost:9092")
topic = client.topics["hello"]

consumer = topic.get_simple_consumer(use_rdkafka=True)

print("hello")
