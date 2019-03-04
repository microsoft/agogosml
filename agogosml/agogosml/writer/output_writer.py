"""OutputWriter class."""
from typing import Callable
from typing import Optional

from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.common.listener_client import ListenerClient
from agogosml.utils.logger import Logger


class OutputWriter:
    """OutputWriter class."""

    def __init__(self, streaming_client: AbstractStreamingClient,
                 listener: ListenerClient):
        """Accept incoming messages and route them to a configured output."""
        self.messaging_client = streaming_client
        self.listener = listener
        self.logger = Logger()

    def on_message_received(self, message: str) -> bool:
        """Send messages onwards to a streaming client."""
        success = self.messaging_client.send(message)
        self.logger.event('output.message.received', {'success': str(success)})
        return success

    def start_incoming_messages(self, callback: Optional[Callable[[str], bool]] = None):
        """Start accepting messages."""
        self.logger.event('output.lifecycle.start')
        self.listener.start(callback or self.on_message_received)

    def stop_incoming_messages(self):
        """Stop accepting messages."""
        self.listener.stop()
        self.logger.event('output.lifecycle.stop')
