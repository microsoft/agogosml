# -*- coding: utf-8 -*-
"""Tests for `kafka_streaming_client` module."""

from dotenv import load_dotenv
import os
import pytest
from agogosml.common.kafka_streaming_client import KafkaStreamingClient

load_dotenv()

test_messages = [
    '{"key": "dfkdsflk", "intValue": 23}',
    '{"key": "kjjioud", "intValue": 73}',
    '{"key": "ewrfsdere", "intValue": 5}',
    '{"key": "dfsadfs", "intValue": 30}',
    '{"key": "dfkdsflk", "intValue": 23}',
    '{"key": "kjjioud", "intValue": 73}',
    '{"key": "ewrfsdere", "intValue": 10}',
    '{"key": "dfsadfs", "intValue": 10}'
]


@pytest.mark.integration
def test_send_receive():
    send_config = {
        "KAFKA_TOPIC": os.getenv("KAFKA_TOPIC"),
        "KAFKA_ADDRESS": os.getenv("KAFKA_ADDRESS"),
    }
    send_client = KafkaStreamingClient(send_config)

    for message in test_messages:
        send_client.send(message)

    send_client.stop()

    receive_config = {
        "KAFKA_TOPIC": os.getenv("KAFKA_TOPIC"),
        "KAFKA_ADDRESS": os.getenv("KAFKA_ADDRESS"),
        "KAFKA_CONSUMER_GROUP": os.getenv("KAFKA_CONSUMER_GROUP"),
        "TIMEOUT": 20
    }
    receive_client = KafkaStreamingClient(receive_config)

    received_messages = []

    def receive_callback(*args, **kwargs):
        for value in args:
            received_messages.append(value.decode("utf-8"))

    receive_client.start_receiving(receive_callback)
    assert len(test_messages) == len(received_messages)
    for msg in received_messages:
        assert msg in test_messages
