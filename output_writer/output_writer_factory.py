"""
Factory and instance resolving for output writer
"""
import os

from agogosml.streaming_client.flask_http_listener_client import FlaskHttpListenerClient
from agogosml.streaming_client.eventhub_streaming_client import EventHubStreamingClient
from agogosml.streaming_client.kafka_streaming_client import KafkaStreamingClient
from output_writer import OutputWriter


class OutputWriterFactory:
    """
    Factory and instance resolving for output writer
    """

    @staticmethod
    def create(config: dict, streaming_client, listener_client):
        """
        Create a new instance
        :param listener_client: An instance of a listener instead of config
        :param streaming_client: An instance of a streaming client instead of config
        :param config: A configuration for output writer
        :return:
        """

        broker = None

        if streaming_client is None:
            if OutputWriterFactory.is_empty(config):
                raise Exception('''
                No config were set for the Output Writer Manager
                ''')

            if config.get("broker") is None:
                raise Exception('''
                broker cannot be empty
                ''')

            client_config = config.get("broker")["config"]
            if config.get("broker")["type"] == "kafka":
                broker = KafkaStreamingClient(client_config)

            if config.get("broker")["type"] == "eventhub":
                broker = EventHubStreamingClient(client_config)

            if broker is None:
                raise Exception('''
                Unknown broker type
                ''')
        else:
            broker = streaming_client

        listener = None

        if listener_client is None:
            port = os.environ['OUTPUT_WRITER_PORT']
            if config.get("listener") is None:
                raise Exception('''
                listener cannot be empty
                ''')

            if config.get("listener")["type"] == "flask":
                listener = FlaskHttpListenerClient(port)

            if listener is None:
                raise Exception('''
                Unknown listener type
                ''')
        else:
            listener = listener_client

        return OutputWriter(broker, listener)

    @staticmethod
    def is_empty(dictionary: dict) -> bool:
        """
        Checks if a dictionary is empty.
        Empty dictionaries resolve to false when
        converted to booleans in Python.
        """
        return not bool(dictionary)
