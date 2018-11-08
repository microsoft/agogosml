"""EventHub streaming client"""

from .abstract_streaming_client import AbstractStreamingClient
from .event_processor import *
from azure.eventhub import EventHubClient, EventData
import asyncio
import logging

logger = logging.getLogger('logger_1')


class EventHubStreamingClient(AbstractStreamingClient):
    def __init__(self, config):
        """
        Class to create an eventhub streaming client instance.

        Args:
            config: dictionary file with all the relevant parameters

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

    def receive(self, timeout=None):
        try:
            loop = asyncio.get_event_loop()
            host = EventProcessorHost(
                                    EventProcessor,
                                    self.client,
                                    self.storage_manager,
                                    ep_params=["param1", "param2"],
                                    eph_options=self.eh_options,
                                    loop=loop)

            # TODO: Changed from wait_and_close in the loop to just run_until_complete
            # TODO: Implement a way of stopping the loop from CI/some external event
            # TODO: How pass back that request was successful?
            tasks = asyncio.gather(
                host.open_async(),
                self.wait_and_close(host, timeout)
            )
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
        "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
        address = "amqps://" + self.namespace + ".servicebus.windows.net/" + self.eventhub
        try:
            client = EventHubClient(address, debug=False, username=self.user, password=self.key)
            sender = client.add_sender()
            client.run()
            try:
                sender.send(EventData(message))
            except:
                raise
            finally:
                client.stop()
        except:
            raise

    @staticmethod
    async def wait_and_close(host, timeout):
        """
        Run EventProcessorHost indefinitely
        """
        if timeout is None:
            while True:
                await asyncio.sleep(1)
            await host.close_async()

        else:
            await asyncio.sleep(timeout)
            await host.close_async()
