"""Broadcast streaming client"""
from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.common.abstract_streaming_client import create_streaming_client_from_config
from agogosml.utils.logger import Logger


class BroadcastStreamingClient(AbstractStreamingClient):
    """Broadcast streaming client"""

    def __init__(self, config: dict):
        """
        Streaming client implementation that broadcases across multiple clients.

        Configuration keys:
          CLIENTS
        """

        self.clients = [
            create_streaming_client_from_config(conf)
            if not isinstance(conf, AbstractStreamingClient) else conf
            for conf in config.get('CLIENTS', [])
        ]

        self.logger = Logger()

    def start_receiving(self, on_message_received_callback):
        self.logger.error('Unexpectedly called %s on %s',
                          self.start_receiving.__name__, self.__class__.__name__)

    def send(self, message):
        success = True
        for client in self.clients:
            success &= client.send(message)
        return success

    def stop(self):
        for client in self.clients:
            client.stop()
