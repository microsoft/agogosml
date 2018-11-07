import sys

from streaming_client.abstract_client_broker import AbstractClientBroker


class EventHubClientBroker(AbstractClientBroker):
    def __init__(self):
        pass

    def topic_exists(self, topic):
        pass

    def create_topic(self, topic, max_partitions=1):
        pass

    def mutate_message(self, message: str):
        pass

    def get_producer(self):
        pass

    def get_consumer(self):
        pass

    def send(self, message: str, *args, **kwargs):
        pass

    def receive(self, *args, **kwargs):
        pass


def is_empty(dictionary: dict) -> bool:
    """
    Checks if a dictionary is empty.
    Empty dictionaries resolve to false when
    converted to booleans in Python.
    """
    return not bool(dictionary)
