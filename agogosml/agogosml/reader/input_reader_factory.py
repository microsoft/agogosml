# -*- coding: utf-8 -*-
""" Factory for InputReader """

from agogosml.common.abstract_streaming_client import create_streaming_client_from_config
from agogosml.common.http_message_sender import HttpMessageSender
from agogosml.utils.logger import Logger

from .input_reader import InputReader

logger = Logger()


class InputReaderFactory:
    """Factory and instance resolving for input reader"""

    @staticmethod
    def create(config: dict, streaming_client=None):
        """Create a new instance of InputReader

        :param config: A configuration for InputReader
        :param streaming_client: Optional, an existing streaming client implementation to use.
        :return InputReader: An instance of an InputReader with streaming_client and message_sender
        """
        if InputReaderFactory.is_empty(config):
            raise Exception('No config were set for the InputReader manager')

        client = streaming_client or create_streaming_client_from_config(config)

        # host and port from the client
        app_host = config.get('APP_HOST')
        app_port = config.get('APP_PORT')

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
