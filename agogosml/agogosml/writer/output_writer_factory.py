# -*- coding: utf-8 -*-
""" Factory for OutputWriter """

from agogosml.common.eventhub_streaming_client import EventHubStreamingClient
from agogosml.common.flask_http_listener_client import FlaskHttpListenerClient
from agogosml.common.kafka_streaming_client import KafkaStreamingClient

from .output_writer import OutputWriter


class OutputWriterFactory:
    """Factory for OutputWriter"""

    @staticmethod
    def create(config: dict, streaming_client=None, listener_client=None):
        """Creates a new instance of OutputWriter.

        :param config: A configuration for OutputWriter.
        :param streaming_client: Optional, an existing streaming client implementation to use.
        :param listener_client: Optional, an existing listener client implementation to use.
        :return OutputWriter: An instance of an OutputWriter with a
        streaming_client and listener.
        """

        client = None

        if OutputWriterFactory.is_empty(config):
            raise Exception('''
            No config was set for the OutputWriterFactory
            ''')

        if streaming_client is None:
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
        else:
            client = streaming_client

        listener = None
        if listener_client is None:
            port = config.get("OUTPUT_WRITER_PORT")
            host = config.get("OUTPUT_WRITER_HOST")

            listener = FlaskHttpListenerClient(port, host)
        else:
            listener = listener_client

        return OutputWriter(client, listener)

    @staticmethod
    def is_empty(dictionary: dict) -> bool:
        """
        Checks if a dictionary is empty.
        Empty dictionaries resolve to false when
        converted to booleans in Python.

        :param dictionary: A dictionary to test.
        :return: True if empty, false otherwise.
        """
        return not bool(dictionary)
