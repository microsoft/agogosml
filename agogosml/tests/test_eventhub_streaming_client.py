# -*- coding: utf-8 -*-
"""Tests for `eventhub_streaming_client` module."""

# TODO: Write mocked unit tests and improve integration tests.

import pytest

from dotenv import load_dotenv
import os
from agogosml.common.eventhub_streaming_client \
    import EventHubStreamingClient

load_dotenv()


def test_send():
    config = {
        "EVENT_HUB_NAMESPACE": os.getenv("EVENT_HUB_NAMESPACE"),
        "EVENT_HUB_NAME": os.getenv("EVENT_HUB_NAME"),
        "EVENT_HUB_SAS_POLICY": os.getenv("EVENT_HUB_SAS_POLICY"),
        "EVENT_HUB_SAS_KEY": os.getenv("EVENT_HUB_SAS_KEY")
    }
    streaming_client = EventHubStreamingClient(config)
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
    for message in messages:
        streaming_client.send(message)
        print(message)

    streaming_client.stop()



def test_receive():
    config = {
        "AZURE_STORAGE_ACCOUNT": os.getenv("AZURE_STORAGE_ACCOUNT"),
        "AZURE_STORAGE_ACCESS_KEY": os.getenv("AZURE_STORAGE_ACCESS_KEY"),
        "LEASE_CONTAINER_NAME": os.getenv("LEASE_CONTAINER_NAME"),
        "EVENT_HUB_NAMESPACE": os.getenv("EVENT_HUB_NAMESPACE"),
        "EVENT_HUB_NAME": os.getenv("EVENT_HUB_NAME"),
        "EVENT_HUB_SAS_POLICY": os.getenv("EVENT_HUB_SAS_POLICY"),
        "EVENT_HUB_SAS_KEY": os.getenv("EVENT_HUB_SAS_KEY"),
        "EVENT_HUB_CONSUMER_GROUP": os.getenv("EVENT_HUB_CONSUMER_GROUP"),
        "APP_HOST": os.getenv("APP_HOST"),
        "APP_PORT": os.getenv("APP_PORT"),
        "TIMEOUT": os.getenv("TIMEOUT")
    }
    streaming_client = EventHubStreamingClient(config)
    
    def start_receiving_callback(*args, **kwargs):
        for value in args:
            print(value)
        for key, value in kwargs.items():
            print("{0} = {1}".format(key, value))
    
    # TODO: Feeding in the HTTP endpoint as env variables,
    # make sure this is correct and add success of post
    streaming_client.start_receiving(start_receiving_callback)
    # assert common is not None


if __name__ == "__main__":
    for i in range(2):
        test_send()
    print("Finished")
