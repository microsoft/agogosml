# -*- coding: utf-8 -*-
""" Factory for OutputWriter """
from agogosml.common.abstract_streaming_client import create_streaming_client_from_config
from agogosml.common.flask_http_listener_client import FlaskHttpListenerClient

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

        if OutputWriterFactory.is_empty(config):
            raise Exception('No config was set for the OutputWriterFactory')

        client = streaming_client or create_streaming_client_from_config(config)

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
