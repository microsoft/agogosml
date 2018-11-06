from flask import Flask, request
import os

from io_base.flask_http_listener_client import FlaskHttpListenerClient
from io_base.eventhub_client_broker import EventHubClientBroker
from io_base.kafka_client_broker import KafkaClientBroker
from output_writer.output_writer import OutputWriter


class OutputWriterFactory:

    @staticmethod
    def create(config: dict):

        if OutputWriterFactory.is_empty(config):
            raise Exception('''
            No config were set for the Output Writer Manager
            ''')

        broker = None

        if config.get("broker") is None:
            raise Exception('''
            broker cannot be empty
            ''')

        if config.get("broker")["type"] == "kafka":
            broker = KafkaClientBroker()

        if config.get("broker.type") == "eventhub":
            broker = EventHubClientBroker()

        if broker is None:
            raise Exception('''
            Unknown broker type
            ''')

        listener = None

        if config.get("listener") is None:
            raise Exception('''
            listener cannot be empty
            ''')

        if config.get("listener")["type"] == "flask":
            listener = FlaskHttpListenerClient()

        if listener is None:
            raise Exception('''
            Unknown listener type
            ''')

        return OutputWriter(broker, listener)

    @staticmethod
    def is_empty(dictionary: dict) -> bool:
        """
        Checks if a dictionary is empty.
        Empty dictionaries resolve to false when
        converted to booleans in Python.
        """
        return not bool(dictionary)
