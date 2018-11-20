# -*- coding: utf-8 -*-
""" Factory for InputReader """
from agogosml.common.eventhub_streaming_client import EventHubStreamingClient
from agogosml.common.http_message_sender import HttpMessageSender
from agogosml.common.kafka_streaming_client import KafkaStreamingClient
from agogosml.utils.logger import Logger
from .input_reader import InputReader

logger = Logger()


class InputReaderFactory:
    """
    Factory and instance resolving for input reader
    """

    @staticmethod
    def create(config: dict):
        """
        Create a new instance of Input Reader

        :param config: A configuration for input reader
        :return InputReader: An instance of an InputReader with streaming_client and message_sender
        """
        if InputReaderFactory.is_empty(config):
            raise Exception('''
            No config were set for the InputReader manager
            ''')

        client = None

        if config.get("client") is None:
            raise Exception('''
            client cannot be empty
            ''')

        client_config = config.get("client")["config"]
        if config.get("client")["type"] == "kafka":
            client = KafkaStreamingClient(client_config)

        if config.get("client")["type"] == "eventhub":
            client = EventHubStreamingClient(client_config)

        if client is None:
            raise Exception('''
            Unknown client type
            ''')

        # host and port from the client
        app_host = config.get("client")["config"]["APP_HOST"]
        app_port = config.get("client")["config"]["APP_PORT"]

        msg_sender = HttpMessageSender(app_host, app_port)

        return InputReader(client, msg_sender)

    @staticmethod
    def is_empty(dictionary: dict) -> bool:
        """
        Checks if a dictionary is empty.
        Empty dictionaries resolve to false when
        converted to booleans in Python.

        :param dictionary: a dictionary to test
        :return: true if empty, false otherwise
        """
        return not bool(dictionary)
