"""EventHub streaming client"""

from .abstract_streaming_client import AbstractStreamingClient
from azure.eventhub import EventHubClient #EventData, EventHubClientAsync, AsyncSender, AsyncReceiver, Offset
from azure.eventprocessorhost import AbstractEventProcessor, AzureStorageCheckpointLeaseManager, \
            EventHubConfig, EventProcessorHost, EPHOptions
import asyncio
import logging

logger = logging.getLogger('logger_1')


class EventProcessor(AbstractEventProcessor):
    """
    Example Implmentation of AbstractEventProcessor
    """

    def __init__(self, params=None):
        """
        Init Event processor
        """
        super().__init__(params)
        self._msg_counter = 0

    async def open_async(self, context):
        """
        Called by processor host to initialize the event processor.
        """
        logger.info("Connection established {}".format(context.partition_id))

    async def close_async(self, context, reason):
        """
        Called by processor host to indicate that the event processor is being stopped.
        :param context: Information about the partition
        :type context: ~azure.eventprocessorhost.PartitionContext
        """
        logger.info("Connection closed (reason {}, id {}, offset {}, sq_number {})".format(
            reason,
            context.partition_id,
            context.offset,
            context.sequence_number))

    async def process_events_async(self, context, messages):
        """TODO: Need to iterate through each message in messages and make an http request
        to the sample app"""
        """
        Called by the processor host when a batch of events has arrived.
        This is where the real work of the event processor is done.
        :param context: Information about the partition
        :type context: ~azure.eventprocessorhost.PartitionContext
        :param messages: The events to be processed.
        :type messages: list[~azure.eventhub.common.EventData]
        """
        logger.info("Events processed {}".format(context.sequence_number))
        await context.checkpoint_async()

    async def process_error_async(self, context, error):
        """
        Called when the underlying client experiences an error while receiving.
        EventProcessorHost will take care of recovering from the error and
        continuing to pump messages,so no action is required from
        :param context: Information about the partition
        :type context: ~azure.eventprocessorhost.PartitionContext
        :param error: The error that occured.
        """
        logger.error("Event Processor Error {!r}".format(error))

async def wait_and_close(host):
    """
    Run EventProcessorHost for 2 minutes then shutdown.
    """
    await asyncio.sleep(60)
    await host.close_async()

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
            self.storage_account_name, self.storage_key, self.lease_container_name)


    def run(self):
        try:
            loop = asyncio.get_event_loop()
            host = EventProcessorHost(
                                    EventProcessor,
                                    self.eh_config,
                                    self.storage_manager,
                                    ep_params=["param1", "param2"],
                                    eph_options=self.eh_options,
                                    loop=loop)

            tasks = asyncio.gather(
                host.open_async(),
                wait_and_close(host)
            )
            loop.run_until_complete(tasks)

        except KeyboardInterrupt:
            # Canceling pending tasks and stopping the loop
            for task in asyncio.Task.all_tasks():
                task.cancel()
            loop.run_forever()
            tasks.exception()

        finally:
            loop.stop()


    def send(self):
        try:
            "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
            address = "amqps://" + self.user + ":" + self.key + "@" + self.namespace + ".servicebus.windows.net/myeventhub"
            client = EventHubClient(address, debug=False, username=self.user, password=self.key)
            sender = client.add_sender(partition="0")
            client.run()

        except:
            pass


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
        #self.producer = self.client.add_sender(*args, **kwargs)
        pass

    def get_consumer(self, *args, **kwargs):
        """
        Creates consumer object.
        """
        #self.consumer = self.client.add_receiver(*args, **kwargs)
        pass

    def mutate_message(message: str):
        """
        Mutates input message.
        """
        #return EventData(message)
        pass

    async def receive(self):
        pass

    # async def _run_send(self, message:str, partition_key:str):
    #     sender = self.client.add_async_sender()
    #     await self.client.run_async()
    #     await self._send(sender, message, partition_key)
    #
    # async def _send(self, sender, message:str, partition_key:str):
    #     mutated_message = self.mutate_message(message)
    #     mutated_message.partition_key = self.mutate_partition_key(partition_key)
    #     await sender.send(mutated_message)

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
