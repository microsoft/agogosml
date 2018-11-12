#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `kafka_streaming_client` module."""
# TODO: Write mocked unit tests and improve integration tests.

from dotenv import load_dotenv
import os
from agogosml.streaming_client import *

load_dotenv()


# def test_send():
#     config = {
#               "KAFKA_ADDRESS": os.getenv("KAFKA_ADDRESS"),
#               "KAFKA_TOPIC": os.getenv("KAFKA_TOPIC")
#               }
#     streaming_client = KafkaStreamingClient(config)
#     messages = [
#         '{"type": "object", "properties": {"key": {"type": "string"}, "intValue": {"type": "integer"}}}',
#         '{"type": "object", "properties": {"key": {"type": "string"}, "intValue": {"type": "integer"}}}'
#     ]
#     for message in messages:
#         streaming_client.send(message)
#         print(message)
#
#     streaming_client.close_send_client()
#
#
# def test_receive():
#     config = {
#               "KAFKA_ADDRESS": os.getenv("KAFKA_ADDRESS"),
#               "KAFKA_CONSUMER_GROUP": os.getenv("KAFKA_CONSUMER_GROUP"),
#               "KAFKA_TOPIC": os.getenv("KAFKA_TOPIC"),
#               "APP_HOST": os.getenv("APP_HOST"),
#               "APP_PORT": os.getenv("APP_PORT")
#               }
#     streaming_client = KafkaStreamingClient(config)
#     # TODO: Feeding in the HTTP endpoint as env variables, make sure this is correct and add success of post
#     streaming_client.receive()
#     assert streaming_client is not None
