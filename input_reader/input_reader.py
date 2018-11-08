"""
Input Reader

--> since this and the input_reader_factory class are super small, should we combine?
or should it follow output_writer structure exactly?
"""

from agogosml.agogosml.streaming_client.abstract_streaming_client import AbstractStreamingClient


class InputReader:  # pylint: disable=too-few-public-methods
    """
    Accepts incoming messages and routes them to a configured output
    """

    def __init__(self, streaming_client: AbstractStreamingClient):
        """
        :param streaming_client: A client that can stream data out
        """
        self.messaging_client = streaming_client

    def receive_messages(self):
        """
        Start receiving messages
        :return:
        """
        self.messaging_client.receive()
