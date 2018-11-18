# -*- coding: utf-8 -*-

"""
InputReader
"""

from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.common.message_sender import MessageSender


class InputReader:  # pylint: disable=too-few-public-methods
    """
    Accepts incoming messages and routes them to a configured output
    """

    def __init__(self, streaming_client: AbstractStreamingClient, message_sender: MessageSender):
        """
        :param streaming_client: A client that can stream data out
        :param message_sender: A message sender that can send messages onwards
        """
        self.message_sender = message_sender
        self.messaging_client = streaming_client

    def start_receiving_messages(self):
        """
        Start receiving messages
        """
        self.messaging_client.start_receiving(self.on_message_received)

    def stop_incoming_messages(self):
        """
        Stop incoming messages from server
        """
        self.messaging_client.stop()

    def on_message_received(self, message):
        """
        Send messages onwards

        :param message: a message to process
        """
        self.message_sender.send(message)
