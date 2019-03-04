"""InputReader."""

from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.common.message_sender import MessageSender
from agogosml.utils.logger import Logger


class InputReader:
    """InputReader."""

    def __init__(self, streaming_client: AbstractStreamingClient, message_sender: MessageSender):
        """Accept an incoming message and route them to a configured output."""
        self.message_sender = message_sender
        self.messaging_client = streaming_client
        self.logger = Logger()

    def start_receiving_messages(self):
        """Start receiving messages from streaming endpoint."""
        self.logger.event('input.lifecycle.start')
        self.messaging_client.start_receiving(self.on_message_received)

    def stop_incoming_messages(self):
        """Stop incoming messages from streaming endpoint."""
        self.messaging_client.stop()
        self.logger.event('input.lifecycle.stop')

    def on_message_received(self, message: str) -> bool:
        """Send messages onwards."""
        result = self.message_sender.send(message)
        if result:
            success = True
        else:
            success = False
            self.handle_send_failure(message)
        self.logger.event('input.message.received', {'success': str(success)})
        return success

    def handle_send_failure(self, message: str):
        """Handle message send failure."""
        self.logger.error('Error while sending message to App %s', message)
        # TODO: Notify...
