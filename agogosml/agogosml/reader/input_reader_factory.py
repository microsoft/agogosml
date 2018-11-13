"""
Factory and instance resolving for input reader
"""
from agogosml.streaming_client.eventhub_streaming_client import EventHubStreamingClient
from agogosml.streaming_client.kafka_streaming_client import KafkaStreamingClient
from .input_reader import InputReader


class InputReaderFactory:
    """
    Factory and instance resolving for input reader
    """

    @staticmethod
    def create(config: dict):
        """
        Create a new instance
        :param config: A configuration for input reader
        :return:
        """
        if InputReaderFactory.is_empty(config):
            raise Exception('''
            No config were set for the input reader Manager
            ''')

        broker = None

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

        # these are NOT in use now as we are passing up the
        # host and port from the client 
        app_host = config.get("broker")["config"]["APP_HOST"]
        app_port = config.get("broker")["config"]["APP_PORT"]

        return InputReader(broker, app_host, app_port)

    @staticmethod
    def is_empty(dictionary: dict) -> bool:
        """
        Checks if a dictionary is empty.
        Empty dictionaries resolve to false when
        converted to booleans in Python.
        """
        return not bool(dictionary)
