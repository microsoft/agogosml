"""EventHub streaming client"""

from .abstract_streaming_client import AbstractStreamingClient
#from azure.eventhub import EventData, EventHubClientAsync, AsyncSender, AsyncReceiver, Offset
from azure.eventprocessorhost import AbstractEventProcessor, AzureStorageCheckpointLeaseManager, \
            EventHubConfig, EventProcessorHost, EPHOptions
import asyncio


class EventHubStreamingClient(AbstractStreamingClient):
    def __init__(self, config):
        """
        Class to create an eventhub streaming client instance.

        Args:
            address: Address string can be in either of these formats:
                    "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
                    "amqps://<mynamespace>.servicebus.windows.net/myeventhub".
            user: User account string.
            key: A name space SAS key string.

        TODO: Change the code to use eventprocessorhub
        watch out for multiple readers on the same partition as these can receive duplicate messages
        make sure you only have one active receiver on a partition per consumer group
        offset useful for knowing where to read from (client side cursor) - checkpointing (reader must keep track)
        """
        self.config = config
        self.storage_account_name = self.config.get("AZURE_STORAGE_ACCOUNT")
        self.storage_key = self.config.get("AZURE_STORAGE_ACCESS_KEY")
        self.lease_container_name = "leases"
        self.namespace = self.config.get("EVENT_HUB_NAMESPACE")
        self.eventhub = self.config.get("EVENT_HUB_NAME")
        self.user = self.config.get("EVENT_HUB_SAS_POLICY")
        self.key = self.config.get("EVENT_HUB_SAS_KEY")

        self.client = EventHubConfig(self.namespace, self.eventhub, self.user, self.key, consumer_group="$default")
        self.eh_options = EPHOptions()
        self.eh_options.release_pump_on_timeout = True
        self.eh_options.debug_trace = False
        self.storage_manager = AzureStorageCheckpointLeaseManager(
            STORAGE_ACCOUNT_NAME, STORAGE_KEY, LEASE_CONTAINER_NAME)
        
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
        
    def mutate_message(message: str):
        """
        Mutates input message.
        """
        return EventData(message)
    
    def mutate_partition_key(self, partition_key):
        return partition_key.encode("utf-8")
    
    async def _run_send(self, message:str, partition_key:str):
        sender = self.client.add_async_sender()
        await self.client.run_async()
        await self._send(sender, message, partition_key)
        
    async def _send(self, sender, message:str, partition_key:str):
        mutated_message = self.mutate_message(message)
        mutated_message.partition_key = self.mutate_partition_key(partition_key)
        await sender.send(mutated_message)
            
    # def send(self, message: str, partition_key: str, *args, **kwargs):
    #     """
    #      Upload a message to a eventhub topic.
    #
    #     Args:
    #         message: A string input to upload to eventhub.
    #     """
    #     '''
    #     TODO:
    #     We are going to need documentation for Eventhub
    #     to ensure proper syntax is clear
    #
    #     '''
    #     if not isinstance(message, str):
    #         raise TypeError('str type expected for message')
    #
    #     try:
    #         loop = asyncio.get_event_loop()
    #         tasks = asyncio.gather(
    #             self._run_send(message, partition_key),
    #             self._run_send(message, partition_key))
    #         loop.run_until_complete(tasks)
    #         loop.run_until_complete(self.client.stop_async())
    #         loop.close()
    #
    #     except KeyboardInterrupt:
    #         pass
    #
    # async def _receiver(self, partition):
    #     OFFSET = Offset("-1")
    #     receiver = self.client.add_async_receiver(self.consumer_group, partition, OFFSET, prefetch=5)
    #     await self.client.run_async()
    #     for event_data in await receiver.receive(timeout=10):
    #         last_offset = event_data.offset
    #         last_sn = event_data.sequence_number
    #
    # def receive(self):
    #     try:
    #         loop = asyncio.get_event_loop()
    #         tasks = [
    #             asyncio.ensure_future(self._receive("0")),
    #             asyncio.ensure_future(self._receive("1"))]
    #         loop.run_until_complete(asyncio.wait(tasks))
    #         loop.run_until_complete(self.client.stop_async())
    #         loop.close()
    #
    #     except KeyboardInterrupt:
    #         pass
