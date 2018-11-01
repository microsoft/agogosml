from confluent_kafka import Producer, Consumer, admin
from azure.eventhub import EventHubClient, EventData


def is_empty(dictionary: dict) -> bool:
    """
    empty dictionaries resolve to false when
    converted to booleans in Python.
    """
    return not bool(dictionary)


class ClientBroker:
    def __init__(framework: str,
                 config={}: dict,
                 address='': str,
                 user='': str,
                 key='': str,
                 topic='': str):
        """
        If you are using confluent_kafka make sure to 
        set your config based on the docs found here:
        https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
        """
        self.topic = topic
        self.framework = framework
        if framework == 'kafka':
            if is_empty(config):
                raise Exception('''
                Hosts must be defined to use kafka!
                ''')
            if config.get("bootstrap.servers") is None:
                raise Exception('''
                bootstrap.servers must be defined with at least one broker.
                ''')
            if config.get("group.id") is None:
                raise Exception('''
                group.id must be defined with some group id
                ''')
            self.admin = admin.AdminClient(config)
            self.config = config
        elif framework == 'eventhub':
            if address == '' or user=='' or key=='':
                raise Exception('''
                Must include address, user, key for eventhub!
                ''')
            self.client = EventHubClient(address, username=user, password=key) 

            
    def topic_exists(self, topic):
        result = self.admin.create_topics(
            [admin.NewTopic(topic, 1)],
            validate_only=True
        )
        return result[topic].result() is not None

    
    def create_topic(self, topic):
        if not self.topic_exists(topic):
            self.admin.create_topics([admin.NewTopic(topic, 1)])
        # add in functionality for Eventhub client
            
    def get_producer(self, *args, **kwargs):
        '''
        TODO:
        We are going to need documentation for kafka & Eventhub
        to ensure proper syntax is clear

        We should be explicit that the style is:
        TODO: fill in [PARAMS GO HERE] with correct examples from
        respective frameworks
        framework = Framework([PARAMS GO HERE])
        framework.get_producer([PARAMS GO HERE])
        framework.send(message, [PARAMS GO HERE])
        '''
        if self.framework == 'kafka':
            self.producer = Producer(self.config)
        if self.framework == 'eventhub':
            self.producer = self.client.add_sender(*args, **kwargs)

            
    def get_consumer(self, *args, **kwargs):
        '''
        TODO:
        We are going to need documentation for kafka & Eventhub
        to ensure proper syntax is clear

        Assumption: We are assuming a high throughput system.
        If you are using this for lower throughput tasks use
        simple_consumer (for kafka).
        
        TODO:
        Make sure to note that the args, kwargs for eventhub and kafka are _very_
        different
        '''
        if self.framework == 'kafka':
            self.consumer = Consumer(self.config)
        if self.framework == 'eventhub':
            self.consumer = self.client.add_receiver(*args, **kwargs)
            

    def mutate_message(self, message: str):
        if self.framework == 'kafka':
            return message.encode('utf-8')
        if self.framework == 'eventhub':
            return EventData(message)

        
    async def send(self, message: str, *args, **kwargs):
        '''
        TODO:
        We are going to need documentation for kafka & Eventhub
        to ensure proper syntax is clear

        '''
        if not isinstance(message, str):
            raise TypeError('str type expected for message')
        mutated_message = self.mutate_message(message)
        if self.framework == 'kafka':
            self.producer.poll(0)
            self.producer.produce(self.mutated_message, *args, **kwargs)
        if self.framework == 'eventhub':
            self.client.run()
            try:
                self.producer.send(self.mutated_message)
            except:
                pass
            finally:
                await client.stop()

                
    async def receive(self, message: str, *args, **kwargs):
        '''
        TODO:
        We are going to need documentation for kafka & Eventhub
        to ensure proper syntax is clear

        ''' 
        if not isinstance(message, str):
            raise TypeError('str type expected for message')
        mutated_message = self.mutate_message(message)
        if self.framework == 'kafka':
            self.consumer.subscribe([self.topic])
            while True:
                #NEED OFFSETS/CHECKPOINTS!!!
                message = self.consumer.poll(1/sys.float_info.max)

                if message is None:
                    continue

                if message.error():
                    return message.error().code()

                yield message
        # TODO:
        # How do we close out the consumer stream when we've seen all objects
        # / Do we even what to do that?
        # question to Itye + Tomer
        if self.framework == 'eventhub':
            consumer = self.get_consumer()
            self.client.run()
            try:
                self.consumer.receive())
            except:
                pass
            finally:
                await client.stop()
    

