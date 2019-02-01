from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.common.message_sender import MessageSender
from agogosml.utils.logger import Logger

logger = Logger()


class InputReader:
    """Accepts incoming messages and routes them to a configured output"""

    def __init__(self, streaming_client: AbstractStreamingClient, message_sender: MessageSender):
        self.message_sender = message_sender
        self.messaging_client = streaming_client

    def start_receiving_messages(self):
        logger.event('input.lifecycle.start')
        self.messaging_client.start_receiving(self.on_message_received)

    def stop_incoming_messages(self):
        self.messaging_client.stop()
        logger.event('input.lifecycle.stop')

    def on_message_received(self, message):
        result = self.message_sender.send(message)
        if result:
            success = True
        else:
            success = False
            self.handle_send_failure(message)
        logger.event('input.message.received', {'success': str(success)})
        return success

    def handle_send_failure(self, message):
        logger.error('Error while sending message to App')
        # Notify...
