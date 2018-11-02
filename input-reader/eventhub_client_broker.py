from abstract_client_broker import AbstractClientBroker
from azure.eventhub import EventHubClient, EventData

class EventHubClientBroker(AbstractClientBroker):
    def __init__(self,
                 address='': str,
                 user='': str,
                 key='': str):
        """
        Class to create an eventhub client broker instance.

        Args:
            address: Address string can be in either of these formats:
                    "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
                    "amqps://<mynamespace>.servicebus.windows.net/myeventhub".
            user: User account string.
            key: A name space SAS key string.

        """
        if address == '' or user == '' or key == '':
            raise Exception('''
            Must include address, user, key for eventhub!
            ''')
        self.client = EventHubClient(address, username=user, password=key)

    def create_topic(self, topic):
        """
        Creates a topic in eventhub.

        Args:
            topic: A string topic.

        """
        # add in functionality for Eventhub client
        pass

    def get_producer(self, *args, **kwargs):
        """
        Creates producer object.
        """
        self.producer = self.client.add_sender(*args, **kwargs)

    def get_consumer(self, *args, **kwargs):
        """
        Creates consumer object.
        """
        self.consumer = self.client.add_receiver(*args, **kwargs)

    def mutate_message(self, message: str):
        """
        Mutates input message.
        """
        return EventData(message)


    async def send(self, message: str, *args, **kwargs):
        """
         Upload a message to a eventhub topic.

        Args:
            message: A string input to upload to eventhub.
        """
        '''
        TODO:
        We are going to need documentation forEventhub
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
        """
        Receive messages from a eventhub topic.
        """
        '''
        TODO:
        We are going to need documentation for Eventhub
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
