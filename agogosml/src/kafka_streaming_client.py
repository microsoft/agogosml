"""Kafka client broker"""

from abstract_client_broker import AbstractClientBroker
from confluent_kafka import Producer, Consumer, admin
import sys
from confluent_kafka import KafkaException, KafkaError


class KafkaClientBroker(AbstractClientBroker):
    def __init__(self, config):
        """
        Class to create a kafka client broker instance.

        Args:
            config: A dict config file with following structure:
                    config = {
                                'bootstrap.servers': '127.0.0.1:9092',
                                'group.id': 'group1',
                                'enable.auto.commit': False
                            }
                    Must specify "bootstrap.servers" and "group.id".
                    Docs here https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
            topic: A string kafka topic.
        """
        self.config = config
        if is_empty(self.config):
            raise Exception('''
            Hosts must be defined to use kafka!
            ''')
        if self.config.get("bootstrap.servers") is None:
            raise Exception('''
            bootstrap.servers must be defined with at least one broker.
            ''')
        if self.config.get("group.id") is None:
            raise Exception('''
            group.id must be defined with some group id
            ''')
        self.admin = admin.AdminClient(self.config)
        self.producer = Producer(self.config)
        self.consumer = Consumer(self.config)

    def set_topic(self, topic):
        self.topic = topic
        
    def mutate_message(self, message: str):
        """
        Mutate the input string message.

        Args:
            message: A string input.
        """
        return message.encode('utf-8')

    def send(self, message: str, *args, **kwargs):
        """
        Upload a message to a kafka topic.

        Args:
            message: A string input to upload to kafka.
        """
        if not isinstance(message, str):
            raise TypeError('str type expected for message')
        mutated_message = self.mutate_message(message)
        self.producer.poll(0)
        self.producer.produce(self.topic, mutated_message, *args, **kwargs)
        
    def receive(self, *args, **kwargs):
        """
        Receive messages from a kafka topic.
        """
        '''
        TODO:
        We are going to need documentation for Kafka
        to ensure proper syntax is clear
        
        '''
        self.consumer.subscribe([self.topic])
        logging.info("subscribed")
        # Read messages from Kafka, print to stdout
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    # Error or event
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write(
                            '%% %s [%d] reached end at offset %d\n' %
                            (msg.topic(), msg.partition(), msg.offset()))
                    else:
                        # Error
                        raise KafkaException(msg.error())
                else:
                    # Proper message
                    sys.stderr.write('%% %s [%d] at offset %d with key %s:\n'
                                     % (msg.topic(), msg.partition(),
                                        msg.offset(), str(msg.key())))
                    t = msg.value()
                    self.consumer.commit(msg)
                    return t

        except KeyboardInterrupt:
            sys.stderr.write('%% Aborted by user\n')

        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()
            
def is_empty(dictionary: dict) -> bool:
    """
    Checks if a dictionary is empty.
    Empty dictionaries resolve to false when
    converted to booleans in Python.
    """
    return not bool(dictionary)
