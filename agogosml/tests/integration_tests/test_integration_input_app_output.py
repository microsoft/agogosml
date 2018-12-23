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
from tests.client_mocks import StreamingClientMock, HttpClientMock
from tests.integration_tests.test_app import TestApp

load_dotenv()


@pytest.fixture
def mock_streaming_client():
    return StreamingClientMock()


@pytest.fixture
def mock_listener_client():
    return HttpClientMock(0)


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
    input_client_mock = StreamingClientMock()
    ir_config = {
        'APP_PORT': os.getenv("APP_PORT"),
        'APP_HOST': os.getenv("APP_HOST"),
    }
    print('Creating reader')
    ir = InputReaderFactory.create(ir_config, input_client_mock)
    print('start_receiving_messages')
    ir.start_receiving_messages()

    # setup app
    app = TestApp(os.getenv("APP_PORT"),
                  os.getenv("APP_HOST"),
                  os.getenv("OUTPUT_WRITER_PORT"),
                  os.getenv("OUTPUT_WRITER_HOST"))
    app.start()

    # setup output
    ow_config = {
        'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
        'OUTPUT_WRITER_HOST': os.getenv("OUTPUT_WRITER_HOST"),
    }

    print('Creating writer')
    output_client_mock = StreamingClientMock()
    ow = OutputWriterFactory.create(ow_config, output_client_mock, None)
    print('start_incoming_messages')
    ow.start_incoming_messages()

    print('sending test message to reader')
    test_msg = str(time.clock())
    # send a message from INPUT reader, and expect it to flow in the pipeline,
    # and eventually be picked up by the output writer
    input_client_mock.fake_incoming_message_from_streaming(test_msg)
    last_msg = output_client_mock.get_last_msg()

    assert last_msg == test_msg
    ir.stop_incoming_messages()
    ow.stop_incoming_messages()
