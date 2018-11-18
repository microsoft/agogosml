# -*- coding: utf-8 -*-

"""
Factory for OutputWriter
"""

import os

from agogosml.common.flask_http_listener_client import FlaskHttpListenerClient
from agogosml.common.eventhub_streaming_client import EventHubStreamingClient
from agogosml.common.kafka_streaming_client import KafkaStreamingClient
from .output_writer import OutputWriter


class OutputWriterFactory:
    """
    Factory for OutputWriter
    """

    @staticmethod
    def create(config: dict):
        """
        Create a new instance
        :param config: A configuration for output writer
        :return OutputWriter: An instance of an OutputWriter with a
            streaming_client and listener
        """

        client = None

        if OutputWriterFactory.is_empty(config):
            raise Exception('''
            No config was set for the OutputWriterFactory
            ''')

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

        port = os.environ['OUTPUT_WRITER_PORT']
        listener = FlaskHttpListenerClient(port)

        return OutputWriter(client, listener)

    @staticmethod
    def is_empty(dictionary: dict) -> bool:
        """
        Checks if a dictionary is empty.
        Empty dictionaries resolve to false when
        converted to booleans in Python.
        """
        return not bool(dictionary)
