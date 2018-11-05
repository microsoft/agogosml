from pykafka import KafkaClient
from azure.eventhub import EventHubClient, EventData

class Broker:
    def __init__(broker: str,
                 hosts='': str,
                 address='': str,
                 user='': str,
                 key='': str):
        self.broker = broker
        if broker == 'kafka':
            if hosts == '':
                raise Exception('''
                Hosts must be defined to use kafka!
                ''')
            self.client = KafkaClient(hosts=hosts)
        elif broker == 'eventhub':
            if address == '' or user=='' or key=='':
                raise Exception('''
                Must include address, user, key for eventhub!
                ''')
            self.client = EventHubClient(address, username=user, password=key) 

    
    def get_producer(self, *args, **kwargs):
        '''
        TODO:
        We are going to need documentation for kafka & Eventhub
        to ensure proper syntax is clear

        We should be explicit that the style is:
        TODO: fill in [PARAMS GO HERE] with correct examples from
        respective brokers
        broker = Broker([PARAMS GO HERE])
        broker.get_producer([PARAMS GO HERE])
        broker.send(message, [PARAMS GO HERE])
        '''
        if self.broker == 'kafka':
            self.producer = self.client.get_producer(*args, **kwargs)
        if self.broker == 'eventhub':
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
        if self.broker == 'kafka':
            self.producer = self.client.get_balanced_consumer(*args, **kwargs)
        if self.broker == 'eventhub':
            self.producer = self.client.add_receiver(*args, **kwargs)
            

    def mutate_message(self, message: str):
        if self.broker == 'kafka':
            return message.encode()
        if self.broker == 'eventhub':
            return EventData(message)

        
    def send(self, message: str, *args, **kwargs):
        '''
        TODO:
        We are going to need documentation for kafka & Eventhub
        to ensure proper syntax is clear

        '''
        if not isinstance(message, str):
            raise TypeError('str type expected for message')
        mutated_message = self.mutate_message(message)
        if self.broker == 'kafka':
            self.producer.produce(self.mutated_message), *args, **kwargs)
        if self.broker == 'eventhub':
            self.client.run()
            try:
                self.producer.send(self.mutated_message))/
            except:
                pass
            finally:
                client.stop()

                
    def receive(self, message: str, *args, **kwargs):
        '''
        TODO:
        We are going to need documentation for kafka & Eventhub
        to ensure proper syntax is clear

        '''
        if not isinstance(message, str):
            raise TypeError('str type expected for message')
        mutated_message = self.mutate_message(message)
        if self.broker == 'kafka':
            consumer.produce(self.mutated_message), *args, **kwargs)
            
        if self.broker == 'eventhub':
            consumer = self.get_cunsumer()
            self.client.run()
            try:
                self.consumer.receive())
            except:
                pass
            finally:
                client.stop()
    

