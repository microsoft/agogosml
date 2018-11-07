import os
import threading

import requests
import pytest

from agogosml.agogosml.streaming_client.abstract_streaming_client import AbstractStreamingClient
from input_reader.input_reader_factory import InputReaderFactory
from agogosml.agogosml.streaming_client.kafka_streaming_client import KafkaStreamingClient


class ClientMessagingMock(AbstractStreamingClient):

    def __init__(self):
        pass

    def mutate_message(self, message: str):
        pass

    def get_producer(self):
        pass

    def get_consumer(self):
        pass

    async def send(self):
        pass

    async def receive(self, message: str):
        pass


def test_when_known_broker_instance_created():
    config = {
        'broker': {
            'type': 'kafka',
            'config': {
                'bootstrap.servers': '127.0.0.1:9092',
                'group.id': ''
            },
            'args': {
                'topic': 'test'
            }},
    }
    owm = OutputWriterFactory.create(config)
    assert owm is not None


def test_when_unknown_broker_throw():
    config = {'broker': {'type': 'aaa'}}
    with pytest.raises(Exception):
        owm = InputReaderFactory.create(config)


async def test_integration():
    config = {
        'broker': {
            'type': 'kafka',
            'config': {
                'bootstrap.servers': '127.0.0.1:9092',
                'group.id': ''
            },
            'args': {
                'topic': 'test'
            }},
        'listener': {
            'type': 'flask'
        }
    }
    owm = InputReaderFactory.create(config)


if __name__ == '__main__':
    test_when_known_broker_instance_created()
    test_when_unknown_broker_throw()