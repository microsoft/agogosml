"""
Input Reader

--> since this and the input_reader_factory class are super small, should we combine?
or should it follow output_writer structure exactly?
"""

from agogosml.streaming_client.abstract_streaming_client import AbstractStreamingClient
from agogosml.utils.send_utils import send_message


class InputReader:  # pylint: disable=too-few-public-methods
    """
    Accepts incoming messages and routes them to a configured output
    """

    def __init__(self, streaming_client: AbstractStreamingClient, host: str, port: str): 
        """
        :param streaming_client: A client that can stream data out
        """
        self.messaging_client = streaming_client
        self.messaging_client.message_callback = self.send_message_callback
        # self.host = host
        # self.port = port

    def receive_messages(self):
        """
        Start receiving messages
        :return:
        """
        self.messaging_client.receive()
    
    def stop_incoming_messages(self):
        """
        Stop incoming messages from server
        """
        self.messaging_client.close_send_client()

    def send_message_callback(self, msg, host, port):
        """
        Send messages to  
        """
        send_message(msg, host, port)
