from .abstract_streaming_client import AbstractStreamingClient
from .abstract_streaming_client import create_streaming_client_from_config


class BroadcastStreamingClient(AbstractStreamingClient):
    def __init__(self, config: dict):
        """
        Class to create a BroadcastStreamingClient instance.

        Configuration keys:
          CLIENTS

        :param config: Dictionary file with all the relevant parameters.
        """

        self.clients = [
            create_streaming_client_from_config(conf)
            if not isinstance(conf, AbstractStreamingClient) else conf
            for conf in config.get('CLIENTS', [])
        ]

    def start_receiving(self, on_message_received_callback):
        """
        Receive messages from all the clients

        :param on_message_received_callback: Callback function.
        """
        raise NotImplementedError

    def send(self, message):
        """
        Send a message to all the clients

        :param message: A string input to upload to event hub.
        """
        success = True
        for client in self.clients:
            success &= client.send(message)
        return success

    def stop(self):
        for client in self.clients:
            client.stop()
