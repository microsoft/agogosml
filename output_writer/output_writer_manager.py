from flask import Flask, request
import os

from io_base.FlaskHttpListener import FlaskHttpListener
from io_base.eventhub_client_broker import EventHubClientBroker
from io_base.kafka_client_broker import KafkaClientBroker


class OutputWriterManager:
    def __init__(self, config):
        self.config = config

        if self.is_empty(self.config):
            raise Exception('''
            No config were set for the Output Writer Manager
            ''')

        if self.config.get("broker") is None:
            raise Exception('''
            broker cannot be empty
            ''')

        if self.config.get("broker")["type"] == "kafka":
            self.broker = KafkaClientBroker()

        if self.config.get("broker.type") == "eventhub":
            self.broker = EventHubClientBroker()

        if self.broker is None:
            raise Exception('''
            Unknown broker type
            ''')

        if self.config.get("listener") is None:
            raise Exception('''
            listener cannot be empty
            ''')

        if self.config.get("listener")["type"] == "flask":
            self.listener = FlaskHttpListener()

        if self.listener is None:
            raise Exception('''
            Unknown listener type
            ''')

        pass

    def start_incoming_messages(self):
        port = os.environ['OUTPUT_READER_PORT']
        self.listener.start(port, self.broker)
        pass

    def stop_incoming_messages(self):
        self.listener.stop()
        pass

    @staticmethod
    def is_empty(dictionary: dict) -> bool:
        """
        Checks if a dictionary is empty.
        Empty dictionaries resolve to false when
        converted to booleans in Python.
        """
        return not bool(dictionary)
