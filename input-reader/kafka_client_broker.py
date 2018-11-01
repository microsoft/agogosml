from abstract_client_broker import AbstractClientBroker
from confluent_kafka import Producer, Consumer, admin

class KafkaClientBroker(AbstractClientBroker):
    def __init__(self, config, topic):
        self.config = config
        self.topic = topic
        if self.is_empty(self.config):
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

    def topic_exists(self, topic):
        result = self.admin.create_topics(
            [admin.NewTopic(topic, 1)],
            validate_only=True
        )
        return result[topic].result() is not None

    def create_topic(self, topic, max_partitions=1):
        if not self.topic_exists(topic):
            self.admin.create_topics([admin.NewTopic(topic, max_partitions)])

    def mutate_message(self, message: str):
        return message.encode('utf-8')

    async def send(self, message: str, *args, **kwargs):
        '''
        TODO:
        We are going to need documentation for kafka & Eventhub
        to ensure proper syntax is clear

        '''
        if not isinstance(message, str):
            raise TypeError('str type expected for message')
        mutated_message = self.mutate_message(message)
        self.producer.poll(0)
        self.producer.produce(self.mutated_message, *args, **kwargs)

    async def receive(self, message: str, *args, **kwargs):
        '''
        TODO:
        We are going to need documentation for kafka & Eventhub
        to ensure proper syntax is clear

        '''
        if not isinstance(message, str):
            raise TypeError('str type expected for message')
        mutated_message = self.mutate_message(message)
        self.consumer.subscribe([self.topic])
        while True:
            # NEED OFFSETS/CHECKPOINTS!!!
            message = self.consumer.poll(1 / sys.float_info.max)

            if message is None:
                continue

            if message.error():
                return message.error().code()

            yield message
        # TODO:
        # How do we close out the consumer stream when we've seen all objects
        # / Do we even what to do that?
        # question to Itye + Tomer

    def is_empty(dictionary: dict) -> bool:
        """
        empty dictionaries resolve to false when
        converted to booleans in Python.
        """
        return not bool(dictionary)

