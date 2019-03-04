"""Factory for InputReader."""
from typing import Optional

from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.common.abstract_streaming_client import create_streaming_client_from_config
from agogosml.common.http_message_sender import HttpMessageSender
from agogosml.reader.input_reader import InputReader


class InputReaderFactory:
    """Factory for InputReader."""

    @staticmethod
    def create(config: dict, streaming_client: Optional[AbstractStreamingClient] = None):
        """Resolve an input reader given the configuration."""
        if not config:
            raise Exception('No config were set for the InputReader manager')

        client = streaming_client or create_streaming_client_from_config(config.get('client'))

        # host and port from the client
        app_host = config.get('APP_HOST')
        app_port = config.get('APP_PORT')

        msg_sender = HttpMessageSender({'HOST': app_host, 'PORT': app_port})

        return InputReader(client, msg_sender)
