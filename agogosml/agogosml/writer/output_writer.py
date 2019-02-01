from typing import Callable
from typing import Optional

from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.common.listener_client import ListenerClient
from agogosml.utils.logger import Logger

logger = Logger()

Callback = Callable[[str], bool]


class OutputWriter:
    """Accepts incoming messages and routes them to a configured output."""

    def __init__(self, streaming_client: AbstractStreamingClient,
                 listener: ListenerClient):
        self.messaging_client = streaming_client
        self.listener = listener

    def on_message_received(self, message: str) -> bool:
        success = self.messaging_client.send(message)
        logger.event('output.message.received', {'success': str(success)})
        return success

    def start_incoming_messages(self, callback: Optional[Callback] = None):
        logger.event('output.lifecycle.start')
        self.listener.start(callback or self.on_message_received)

    def stop_incoming_messages(self):
        self.listener.stop()
        logger.event('output.lifecycle.stop')
