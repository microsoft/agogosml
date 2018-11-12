#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `eventhub_streaming_client` module."""
# TODO: Write mocked unit tests and improve integration tests.

import pytest
from dotenv import load_dotenv
import os
from agogosml.streaming_client import *

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

    streaming_client.close_send_client()
#
# def test_receive():
#     config = {"AZURE_STORAGE_ACCOUNT": os.getenv("AZURE_STORAGE_ACCOUNT"),
#               "AZURE_STORAGE_ACCESS_KEY": os.getenv("AZURE_STORAGE_ACCESS_KEY"),
#               "LEASE_CONTAINER_NAME": os.getenv("LEASE_CONTAINER_NAME"),
#               "EVENT_HUB_NAMESPACE": os.getenv("EVENT_HUB_NAMESPACE"),
#               "EVENT_HUB_NAME": os.getenv("EVENT_HUB_NAME"),
#               "EVENT_HUB_SAS_POLICY": os.getenv("EVENT_HUB_SAS_POLICY"),
#               "EVENT_HUB_SAS_KEY": os.getenv("EVENT_HUB_SAS_KEY"),
#               "EVENT_HUB_CONSUMER_GROUP": os.getenv("EVENT_HUB_CONSUMER_GROUP"),
#               "APP_HOST": os.getenv("APP_HOST"),
#               "APP_PORT": os.getenv("APP_PORT")
#               }
#     streaming_client = EventHubStreamingClient(config)
#     # TODO: Feeding in the HTTP endpoint as env variables, make sure this is correct and add success of post
#     streaming_client.receive(timeout=2)
#     #assert streaming_client is not None
