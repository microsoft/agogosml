"""
Input Reader

--> since this and the input_reader_factory class are super small, should we combine?
or should it follow output_writer structure exactly?
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
        """
        self.message_sender = message_sender
        self.messaging_client = streaming_client

    def start_receiving_messages(self):
        """
        Start receiving messages
        :return:
        """
        self.messaging_client.start_receiving(self.on_message_received)

    def stop_incoming_messages(self):
        """
        Stop incoming messages from server
        """
        self.messaging_client.stop()

    def on_message_received(self, msg):
        """
        Send messages onwards
        """
        self.message_sender.send(msg)
