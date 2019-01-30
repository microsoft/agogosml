# -*- coding: utf-8 -*-
""" Factory for InputReader """
from functools import lru_cache
from typing import Dict
from typing import Type

from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.common.http_message_sender import HttpMessageSender
from agogosml.utils.imports import find_implementations
from agogosml.utils.logger import Logger

from .input_reader import InputReader

StreamingClientType = Type[AbstractStreamingClient]

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
            raise Exception('''
            No config were set for the InputReader manager
            ''')

        if streaming_client is None:
            if config.get("client") is None:
                raise Exception('''
                client cannot be empty
                ''')

            client_config = config.get("client")["config"]
            client_type = config.get("client")["type"]

            client_class = find_streaming_clients().get(client_type)
            if client_class is None:
                raise Exception('''
                Unknown client type
                ''')

            client = client_class(client_config)
        else:
            client = streaming_client

        # host and port from the client
        app_host = config.get("APP_HOST")
        app_port = config.get("APP_PORT")

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


@lru_cache(maxsize=1)
def find_streaming_clients() -> Dict[str, StreamingClientType]:
    """
    >>> senders = find_streaming_clients()
    >>> sorted(senders.keys())
    ['eventhub', 'kafka', 'mock']
    """
    return {
        client.__name__.replace('StreamingClient', '').lower(): client
        for client in find_implementations(AbstractStreamingClient)
    }
