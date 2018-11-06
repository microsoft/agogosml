import os

from io_base.abstract_client_broker import AbstractClientBroker
from io_base.listener_client import ListenerClient


class OutputWriter:
    def __init__(self, client_broker: AbstractClientBroker, listener: ListenerClient):
        self.messaging_client = client_broker
        self.listener = listener
        pass

    async def on_message_received(self, message: str):
        await self.messaging_client.send(message)
        pass

    def start_incoming_messages(self):
        port = os.environ['OUTPUT_WRITER_PORT']
        self.listener.start(port, self.on_message_received)
        pass

    def stop_incoming_messages(self):
        self.listener.stop()
        pass
