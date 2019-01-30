# -*- coding: utf-8 -*-
""" InputReader """

from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.common.message_sender import MessageSender
from agogosml.utils.logger import Logger

logger = Logger()


class InputReader:
    """Accepts incoming messages and routes them to a configured output"""

    def __init__(self, streaming_client: AbstractStreamingClient, message_sender: MessageSender):
        """
        :param streaming_client: A client that can stream data out
        :param message_sender: A message sender that can send messages onwards
        """
        self.message_sender = message_sender
        self.messaging_client = streaming_client

    def start_receiving_messages(self):
        """Start receiving messages from streaming endpoint"""
        self.messaging_client.start_receiving(self.on_message_received)

    def stop_incoming_messages(self):
        """Stop incoming messages from streaming endpoint"""
        self.messaging_client.stop()

    def on_message_received(self, message):
        """Send messages onwards

        :param message: a message to process
        """
        result = self.message_sender.send(message)
        if result:
            return True
            pass
        else:
            self.handle_send_failure(message)
            return False

    def handle_send_failure(self, message):
        logger.error('Error while sending message to App')
        # Notify...
