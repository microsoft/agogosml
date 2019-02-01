from typing import Optional

from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.common.abstract_streaming_client import create_streaming_client_from_config
from agogosml.common.flask_http_listener_client import FlaskHttpListenerClient
from agogosml.common.listener_client import ListenerClient

from .output_writer import OutputWriter


class OutputWriterFactory:
    @staticmethod
    def create(config: dict,
               streaming_client: Optional[AbstractStreamingClient] = None,
               listener_client: Optional[ListenerClient] = None):
        if not config:
            raise Exception('No config was set for the OutputWriterFactory')

        client = streaming_client or create_streaming_client_from_config(config.get('client'))

        listener = listener_client or FlaskHttpListenerClient({
            'PORT': config.get("OUTPUT_WRITER_PORT"),
            'HOST': config.get("OUTPUT_WRITER_HOST"),
        })

        return OutputWriter(client, listener)
