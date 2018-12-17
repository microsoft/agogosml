import asyncio
import threading
from multiprocessing.pool import ThreadPool
import pytest
import os
import requests
import json
import time
from dotenv import load_dotenv

from agogosml.reader.input_reader import InputReader
from agogosml.reader.input_reader_factory import InputReaderFactory
from agogosml.writer.output_writer import OutputWriter
from agogosml.writer.output_writer_factory import OutputWriterFactory
from agogosml.common.flask_http_listener_client import FlaskHttpListenerClient
from agogosml.common.kafka_streaming_client import KafkaStreamingClient
from agogosml.common.eventhub_streaming_client import EventHubStreamingClient
from tests.client_mocks import ClientMessagingMock, ListenerClientMock

load_dotenv()


@pytest.fixture
def mock_streaming_client():
    return ClientMessagingMock()


@pytest.fixture
def mock_listener_client():
    return ListenerClientMock(0)


@pytest.mark.integration
def test_when_messages_received_in_input_then_all_messages_are_sent_via_output():
    """
    This function tests the integration of input and output.
    It assumes connectivity to streaming client is correct, therefore the steaming client is mocked.
    We look to find that once a message is received, it is send out by the output writer.
    This is the maximal integration test we can have in an isolated environment.
    :return:
    """

    # setup input
    ir_streaming_client = ClientMessagingMock()
    ir_config = {
        'APP_PORT': os.getenv("OUTPUT_WRITER_PORT"),
        'APP_HOST': os.getenv("OUTPUT_WRITER_HOST"),
    }
    print('Creating reader')
    ir = InputReaderFactory.create(ir_config, ir_streaming_client)
    print('start_receiving_messages')
    ir.start_receiving_messages()

    # setup app is skipped.

    # setup output
    ow_config = {
        'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
        'OUTPUT_WRITER_HOST': os.getenv("OUTPUT_WRITER_HOST"),
    }

    print('Creating writer')
    ow_streaming_client = ClientMessagingMock()
    ow = OutputWriterFactory.create(ow_config, ow_streaming_client, None)
    print('start_incoming_messages')
    ow.start_incoming_messages()

    print('sending test message to reader')
    test_msg = str(time.clock())
    # send a message from input reader, and expect it to flow in the pipeline,
    # and eventually be picked up by the output writer
    ir_streaming_client.mock_incoming_message_event(test_msg)
    last_msg = ow_streaming_client.get_last_msg()

    assert last_msg == test_msg
    ir.stop_incoming_messages()
    ow.stop_incoming_messages()
