
"""
Output Writer
"""

from agogosml.agogosml.streaming_client.abstract_streaming_client import AbstractStreamingClient
from agogosml.agogosml.streaming_client.listener_client import ListenerClient


class OutputWriter:
    """
    Accepts incoming messages and routes them to a configured output
    """

    def __init__(self, streaming_client: AbstractStreamingClient, listener: ListenerClient):
        """
        :param streaming_client: A client that can stream data out
        :param listener: A client that accepts incoming messages
        """
        self.messaging_client = streaming_client
        self.listener = listener

    def on_message_received(self, message: str):
        """
        :param message: a message to process
        :return:
        """
        self.messaging_client.send(message)

    def start_incoming_messages(self):
        """
        Start accepting messages
        :return:
        """

        self.listener.start(self.on_message_received)

    def stop_incoming_messages(self):
        """
        Stop accepting messages.
        :return:
        """
        self.listener.stop()