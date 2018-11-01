from abstract_client_broker import AbstractClientBroker
from azure.eventhub import EventHubClient, EventData

class EventHubClientBroker(AbstractClientBroker):
    def __init__(self,
                 address='': str,
                 user='': str,
                 key='': str):
        if address == '' or user == '' or key == '':
            raise Exception('''
            Must include address, user, key for eventhub!
            ''')
        self.client = EventHubClient(address, username=user, password=key)

    def create_topic(self, topic):
        # add in functionality for Eventhub client
        pass

    def get_producer(self, *args, **kwargs):
        self.producer = self.client.add_sender(*args, **kwargs)

    def get_consumer(self, *args, **kwargs):
        self.consumer = self.client.add_receiver(*args, **kwargs)

    def mutate_message(self, message: str):
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
        self.client.run()
        try:
            self.producer.send(mutated_message)
        except:
            pass
        finally:
            await self.client.stop()


    async def receive(self, message: str, *args, **kwargs):
        '''
        TODO:
        We are going to need documentation for kafka & Eventhub
        to ensure proper syntax is clear

        '''
        if not isinstance(message, str):
            raise TypeError('str type expected for message')
        consumer = self.get_consumer()
        self.client.run()
        try:
            self.consumer.receive()
        except:
            pass
        finally:
            await self.client.stop()
