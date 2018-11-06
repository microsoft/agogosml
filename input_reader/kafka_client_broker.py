"""Kafka client broker"""

from pykafka import KafkaClient
import sys



class KafkaClientBroker:
    def __init__(self, hosts):
        """
        Class to create a kafka client broker instance.
        """
        self.client = KafkaClient(hosts=hosts)

    def get_producer(self, consumer_group):
        self.producer = self.client.get_balanced_producer(
            consumer_group=consumer_group,
            use_rdkafka=True,
            zookeeper_connect="127.0.0.1:2181"
        )

    def get_consumer(self, *args, **kwargs):
        self.client.get_balanced_consumer(
            consumer_group=,
            zookeeper_connect="localhost:2181",
            auto_commit-enable=True,
        use_rdkafka=True)
        
    def create_topic(self, topic):
        """
        Creates a new kafka topic given a string input name

        Args:
            topic: A string input.
            max_partitions: Maximum number of partitions to use.
        """
        self.topic = self.client.topics[topic]

    def mutate_message(self, message: str):
        """
        Mutate the input string message.
        
            message: A string input.
        """
        return message.encode()

    def send(self, message: str, *args, **kwargs):
        """
        Upload a message to a kafka topic.

        Args:
            message: A string input to upload to kafka.
        """
        if not isinstance(message, str):
            raise TypeError('str type expected for message')
        mutated_message = self.mutate_message(message)
        self.producer.produce(mutated_message)

    def receive(self, *args, **kwargs):
        """
        Receive messages from a kafka topic.
        """
        '''
        TODO:
        We are going to need documentation for Kafka
        to ensure proper syntax is clear

        '''
        
        
        
            
def is_empty(dictionary: dict) -> bool:
    """
    Checks if a dictionary is empty.
    Empty dictionaries resolve to false when
    converted to booleans in Python.
    """
    return not bool(dictionary)

