"""Event Hub streaming client"""

import asyncio
from typing import Optional

from azure.eventhub import EventData
from azure.eventhub import EventHubClient
from azure.eventprocessorhost import AbstractEventProcessor
from azure.eventprocessorhost import AzureStorageCheckpointLeaseManager
from azure.eventprocessorhost import EPHOptions
from azure.eventprocessorhost import EventHubConfig
from azure.eventprocessorhost import EventProcessorHost

from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.utils.logger import Logger


class EventProcessor(AbstractEventProcessor):
    """EventProcessor host class for Event Hub"""

    def __init__(self, params):
        """Sample Event Hub event processor implementation"""
        super().__init__()
        self.on_message_received_callback = params[0]
        self._msg_counter = 0
        self.logger = Logger()

    async def open_async(self, context):
        """
        Called by processor host to initialize the event processor.
        """
        self.logger.info("Connection established %s", context.partition_id)

    async def close_async(self, context, reason):
        """
        Called by processor host to indicate that the event processor
        is being stopped.

        :param context: Information about the partition.
        :type context: ~azure.eventprocessorhost.PartitionContext
        :param reason: Reason for closing the async loop.
        :type reason: string
        """
        self.logger.info("Connection closed (reason %s, id %s, offset %s, sq_number %s)",
                         reason, context.partition_id, context.offset, context.sequence_number)

    async def process_events_async(self, context, messages):
        """
        Called by the processor host when a batch of events has arrived.
        This is where the real work of the event processor is done.

        :param context: Information about the partition.
        :type context: ~azure.eventprocessorhost.PartitionContext
        :param messages: The events to be processed.
        :type messages: list[~azure.eventhub.common.EventData]
        """
        for message in messages:
            message_json = message.body_as_str(encoding='UTF-8')
            if self.on_message_received_callback is not None:
                self.on_message_received_callback(message_json)
                self.logger.debug("Received message: %s", message_json)
        self.logger.info("Events processed %s", context.sequence_number)
        await context.checkpoint_async()

    async def process_error_async(self, context, error):
        """
        Called when the underlying client experiences an error while receiving.
        EventProcessorHost will take care of recovering from the error and
        continuing to pump messages, so no external action is required.

        :param context: Information about the partition.
        :type context: ~azure.eventprocessorhost.PartitionContext
        :param error: The error that occured.
        """
        self.logger.error("Event Processor Error %s", error)


class EventHubStreamingClient(AbstractStreamingClient):
    """Event Hub streaming client"""

    def __init__(self, config):
        """
        Azure EventHub streaming client implementation.

        Configuration keys:
          AZURE_STORAGE_ACCESS_KEY
          AZURE_STORAGE_ACCOUNT
          EVENT_HUB_CONSUMER_GROUP
          EVENT_HUB_NAME
          EVENT_HUB_NAMESPACE
          EVENT_HUB_SAS_KEY
          EVENT_HUB_SAS_POLICY
          LEASE_CONTAINER_NAME
          TIMEOUT
        """

        storage_account_name = config.get("AZURE_STORAGE_ACCOUNT")
        storage_key = config.get("AZURE_STORAGE_ACCESS_KEY")
        lease_container_name = config.get("LEASE_CONTAINER_NAME")
        namespace = config.get("EVENT_HUB_NAMESPACE")
        eventhub = config.get("EVENT_HUB_NAME")
        consumer_group = config.get("EVENT_HUB_CONSUMER_GROUP", '$default')
        user = config.get("EVENT_HUB_SAS_POLICY")
        key = config.get("EVENT_HUB_SAS_KEY")

        try:
            self.timeout = int(config['TIMEOUT'])
        except (KeyError, ValueError):
            self.timeout = None

        self.logger = Logger()

        # Create EPH Client
        if storage_account_name is not None and storage_key is not None:
            self.eph_client = EventHubConfig(
                sb_name=namespace,
                eh_name=eventhub,
                policy=user,
                sas_key=key,
                consumer_group=consumer_group)
            self.eh_options = EPHOptions()
            self.eh_options.release_pump_on_timeout = True
            self.eh_options.auto_reconnect_on_error = False
            self.eh_options.debug_trace = False
            self.storage_manager = AzureStorageCheckpointLeaseManager(
                storage_account_name, storage_key,
                lease_container_name)

        # Create Send client
        else:
            address = "amqps://" + namespace + \
                      ".servicebus.windows.net/" + eventhub
            try:
                self.send_client = EventHubClient(
                    address,
                    debug=False,
                    username=user,
                    password=key)
                self.sender = self.send_client.add_sender()
                self.send_client.run()
            except Exception as ex:
                self.logger.error('Failed to init EH send client: %s', ex)
                raise

    def start_receiving(self, on_message_received_callback):
        loop = asyncio.get_event_loop()
        try:
            host = EventProcessorHost(
                EventProcessor,
                self.eph_client,
                self.storage_manager,
                ep_params=[on_message_received_callback],
                eph_options=self.eh_options,
                loop=loop)

            tasks = asyncio.gather(host.open_async(),
                                   self.wait_and_close(host, self.timeout))
            loop.run_until_complete(tasks)

        finally:
            loop.stop()

    def send(self, message):
        try:
            self.sender.send(EventData(body=message))
            self.logger.info('Sent message: %s', message)
            return True
        except Exception as ex:
            self.logger.error('Failed to send message to EH: %s', ex)
            return False

    def stop(self):
        try:
            self.send_client.stop()
        except Exception as ex:
            self.logger.error('Failed to close send client: %s', ex)

    @staticmethod
    async def wait_and_close(host: EventProcessorHost, timeout: Optional[float] = None):
        """Run a host indefinitely or until the timeout is reached."""
        if timeout is None:
            while True:
                await asyncio.sleep(1)

        else:
            await asyncio.sleep(timeout)
            await host.close_async()
