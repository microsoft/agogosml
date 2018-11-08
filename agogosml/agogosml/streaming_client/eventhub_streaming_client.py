"""EventHub streaming client"""

from .abstract_streaming_client import AbstractStreamingClient
from .eventhub_processor_events import *
from azure.eventhub import EventHubClient, EventData
from azure.eventprocessorhost import  AzureStorageCheckpointLeaseManager, \
            EventHubConfig, EventProcessorHost, EPHOptions
import asyncio
import logging

logger = logging.getLogger("EH")
logger.setLevel(logging.INFO)


class EventHubStreamingClient(AbstractStreamingClient):
    def __init__(self, config):
        """
        Class to create an eventhub streaming client instance.

        Args:
            config: dictionary file with all the relevant parameters

        """
        super().__init__()
        self.config = config
        self.storage_account_name = self.config.get("AZURE_STORAGE_ACCOUNT")
        self.storage_key = self.config.get("AZURE_STORAGE_ACCESS_KEY")
        self.lease_container_name = self.config.get("LEASE_CONTAINER_NAME")
        self.namespace = self.config.get("EVENT_HUB_NAMESPACE")
        self.eventhub = self.config.get("EVENT_HUB_NAME")
        self.consumer_group = self.config.get("EVENT_HUB_CONSUMER_GROUP")
        self.user = self.config.get("EVENT_HUB_SAS_POLICY")
        self.key = self.config.get("EVENT_HUB_SAS_KEY")
        self.app_host = self.config.get("APP_HOST")
        self.app_port = self.config.get("APP_PORT")

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
            self.eh_options.debug_trace = False
            self.storage_manager = AzureStorageCheckpointLeaseManager(
                self.storage_account_name, self.storage_key,
                self.lease_container_name)

        # Create Send client
        else:
            "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
            address = "amqps://" + self.namespace + ".servicebus.windows.net/" + self.eventhub
            try:
                self.send_client = EventHubClient(
                  address, debug=False, username=self.user, password=self.key)
                self.sender = self.send_client.add_sender()
                self.send_client.run()
            except Exception as e:
                logger.error('Failed to init EH send client: ' + str(e))
                raise

    def receive(self, timeout=None):
        loop = asyncio.get_event_loop()
        try:
            ep = EventProcessor
            ep.app_host = self.app_host
            ep.app_port = self.app_port
            host = EventProcessorHost(
                ep,
                self.eph_client,
                self.storage_manager,
                ep_params=["param1", "param2"],
                eph_options=self.eh_options,
                loop=loop)

            # TODO: Changed from wait_and_close in the loop to just run_until_complete
            # TODO: Implement a way of stopping the loop from CI/some external event
            # TODO: How pass back that request was successful?
            tasks = asyncio.gather(host.open_async(),
                                   self.wait_and_close(host, timeout))
            # Check that is works as expected - ie continues running indefinitely if there are more messages
            loop.run_until_complete(tasks)

        except KeyboardInterrupt:
            # Canceling pending tasks and stopping the loop
            for task in asyncio.Task.all_tasks():
                task.cancel()
            loop.run_forever()
            tasks.exception()

        finally:
            loop.stop()

    def send(self, message):

        try:
            self.sender.send(EventData(message))
        except Exception as e:
            logger.error('Failed to send message to EH: ' + str(e))

    def close_send_client(self):

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
