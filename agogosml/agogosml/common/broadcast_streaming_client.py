from .abstract_streaming_client import AbstractStreamingClient
from .abstract_streaming_client import create_streaming_client_from_config


class BroadcastStreamingClient(AbstractStreamingClient):
    def __init__(self, config: dict):
        """
        Configuration keys:
          CLIENTS
        """

        self.clients = [
            create_streaming_client_from_config(conf)
            if not isinstance(conf, AbstractStreamingClient) else conf
            for conf in config.get('CLIENTS', [])
        ]

    def start_receiving(self, on_message_received_callback):
        raise NotImplementedError

    def send(self, message):
        success = True
        for client in self.clients:
            success &= client.send(message)
        return success

    def stop(self):
        for client in self.clients:
            client.stop()
