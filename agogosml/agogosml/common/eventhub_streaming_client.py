import logging
import asyncio
"""EventHub streaming client"""
from .eventhub_processor_events import EventProcessor
from .abstract_streaming_client import AbstractStreamingClient
from azure.eventhub import EventHubClient, EventData
from azure.eventprocessorhost import AzureStorageCheckpointLeaseManager, \
    EventHubConfig, EventProcessorHost, EPHOptions

logger = logging.getLogger(__name__)


class EventHubStreamingClient(AbstractStreamingClient):
    def __init__(self, config):
        """
        Class to create an eventhub streaming client instance.

        Args:
            config: dictionary file with all the relevant parameters

        """
        super().__init__()
        self.message_callback = None
        self.config = config
        self.storage_account_name = self.config.get("AZURE_STORAGE_ACCOUNT")
        self.storage_key = self.config.get("AZURE_STORAGE_ACCESS_KEY")
        self.lease_container_name = self.config.get("LEASE_CONTAINER_NAME")
        self.namespace = self.config.get("EVENT_HUB_NAMESPACE")
        self.eventhub = self.config.get("EVENT_HUB_NAME")
        self.consumer_group = self.config.get("EVENT_HUB_CONSUMER_GROUP")
        if self.consumer_group is None:
            self.consumer_group = '$default'

        self.user = self.config.get("EVENT_HUB_SAS_POLICY")
        self.key = self.config.get("EVENT_HUB_SAS_KEY")
        if self.config.get("TIMEOUT"):
            try:
                self.timeout = int(self.config.get("TIMEOUT"))
            except ValueError:
                self.timeout = None
        else:
            self.timeout = None

        # Create EPH Client
        if self.storage_account_name is not None and self.storage_key is not None:
            self.eph_client = EventHubConfig(
                self.namespace,
                self.eventhub,
                self.user,
                self.key,
                consumer_group=self.consumer_group)
            self.eh_options = EPHOptions()
            self.eh_options.release_pump_on_timeout = True
            self.eh_options.auto_reconnect_on_error = False
            self.eh_options.debug_trace = False
            self.storage_manager = AzureStorageCheckpointLeaseManager(
                self.storage_account_name, self.storage_key,
                self.lease_container_name)

        # Create Send client
        else:
            address = "amqps://" + self.namespace + \
                      ".servicebus.windows.net/" + self.eventhub
            try:
                self.send_client = EventHubClient(
                    address,
                    debug=False,
                    username=self.user,
                    password=self.key)
                self.sender = self.send_client.add_sender()
                self.send_client.run()
            except Exception as e:
                logger.error('Failed to init EH send client: ' + str(e))
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
            logger.info('Sent message: {}'.format(message))
        except Exception as e:
            logger.error('Failed to send message to EH: ' + str(e))

    def stop(self):
        try:
            self.send_client.stop()
        except Exception as e:
            logger.error('Failed to close send client: ' + str(e))

    @staticmethod
    async def wait_and_close(host, timeout):
        """
        Run EventProcessorHost indefinitely
        """
        if timeout is None:
            while True:
                await asyncio.sleep(1)

        else:
            await asyncio.sleep(timeout)
            await host.close_async()
