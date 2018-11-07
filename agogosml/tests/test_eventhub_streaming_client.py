#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `eventhub_streaming_client` module."""

import pytest
from dotenv import load_dotenv
import os
from agogosml.agogosml.streaming_client import *
load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")


def test_send():
    config = {"AZURE_STORAGE_ACCOUNT": os.getenv("AZURE_STORAGE_ACCOUNT"),
              "AZURE_STORAGE_ACCESS_KEY": os.getenv("AZURE_STORAGE_ACCESS_KEY"),
              "LEASE_CONTAINER_NAME": "leases",
              "EVENT_HUB_NAMESPACE": os.getenv("EVENT_HUB_NAMESPACE"),
              "EVENT_HUB_NAME": os.getenv("EVENT_HUB_NAME"),
              "EVENT_HUB_SAS_POLICY": os.getenv("EVENT_HUB_SAS_POLICY"),
              "EVENT_HUB_SAS_KEY": os.getenv("EVENT_HUB_SAS_KEY")
              }
    streaming_client = EventHubStreamingClient(config)
    #messages = ["making a list", "of various", "messages that", "need to be tested" ]
    messages = [
        {"type": "object", "properties": {"key": {"type": "string"}, "intValue": {"type": "integer"}}},
         {"type": "object", "properties": {"key": {"type": "string"}, "intValue": {"type": "integer"}}}
    ]
    for message in messages:
        streaming_client.send(message)
        print(message)
    print("Successfully sent all the messages")


def test_receive():
    config = {"AZURE_STORAGE_ACCOUNT": os.getenv("AZURE_STORAGE_ACCOUNT"),
              "AZURE_STORAGE_ACCESS_KEY": os.getenv("AZURE_STORAGE_ACCESS_KEY"),
              "LEASE_CONTAINER_NAME": "leases",
              "EVENT_HUB_NAMESPACE": os.getenv("EVENT_HUB_NAMESPACE"),
              "EVENT_HUB_NAME": os.getenv("EVENT_HUB_NAME"),
              "EVENT_HUB_SAS_POLICY": os.getenv("EVENT_HUB_SAS_POLICY"),
              "EVENT_HUB_SAS_KEY": os.getenv("EVENT_HUB_SAS_KEY")
              }
    streaming_client = EventHubStreamingClient(config)
    # TODO: Feeding in the HTTP endpoint as env variables, make sure this is correct and add success of post
    request = streaming_client.receive()
    print("This worked")




