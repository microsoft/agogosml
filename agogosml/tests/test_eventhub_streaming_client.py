# -*- coding: utf-8 -*-
"""Tests for `eventhub_streaming_client` module."""

from dotenv import load_dotenv
import os
import pytest
from agogosml.common.eventhub_streaming_client import EventHubStreamingClient

load_dotenv()

messages = [
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
        "EVENT_HUB_NAMESPACE": os.getenv("EVENT_HUB_NAMESPACE"),
        "EVENT_HUB_NAME": os.getenv("EVENT_HUB_NAME"),
        "EVENT_HUB_SAS_POLICY": os.getenv("EVENT_HUB_SAS_POLICY"),
        "EVENT_HUB_SAS_KEY": os.getenv("EVENT_HUB_SAS_KEY")
    }
    send_client = EventHubStreamingClient(send_config)

    for message in messages:
        send_client.send(message)

    send_client.stop()

    receive_config = {
        "AZURE_STORAGE_ACCOUNT": os.getenv("AZURE_STORAGE_ACCOUNT"),
        "AZURE_STORAGE_ACCESS_KEY": os.getenv("AZURE_STORAGE_ACCESS_KEY"),
        "LEASE_CONTAINER_NAME": os.getenv("LEASE_CONTAINER_NAME"),
        "EVENT_HUB_NAMESPACE": os.getenv("EVENT_HUB_NAMESPACE"),
        "EVENT_HUB_NAME": os.getenv("EVENT_HUB_NAME"),
        "EVENT_HUB_SAS_POLICY": os.getenv("EVENT_HUB_SAS_POLICY"),
        "EVENT_HUB_SAS_KEY": os.getenv("EVENT_HUB_SAS_KEY"),
        "EVENT_HUB_CONSUMER_GROUP": os.getenv("EVENT_HUB_CONSUMER_GROUP"),
        "TIMEOUT": 60
    }
    receive_client = EventHubStreamingClient(receive_config)

    received_messages = []

    def receive_callback(*args, **kwargs):
        for value in args:
            received_messages.append(value)

    receive_client.start_receiving(receive_callback)

    assert len(messages) == len(received_messages)
    for msg in received_messages:
        assert msg in messages
