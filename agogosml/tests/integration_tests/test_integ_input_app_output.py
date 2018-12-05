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


def test_when_messages_received_in_input_then_all_messages_are_sent_via_output():

    # setup input
    ir_streaming_client = ClientMessagingMock()
    ir_config = {
        'APP_HOST': os.getenv("OUTPUT_WRITER_PORT"),
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
    test_msg = 'test'
    ir_streaming_client.mock_incoming_message_event(test_msg)
    last_msg = ow_streaming_client.get_last_msg()

    assert last_msg == test_msg
    ir.stop_incoming_messages()
    ow.stop_incoming_messages()


@pytest.mark.integration
def test_when_configured_event_hub_then_correct_messaging_client_created():
    config = {
        'client': {
            'type': 'eventhub',
            'config': {
                'EVENT_HUB_NAMESPACE': os.getenv("EVENT_HUB_NAMESPACE"),
                'EVENT_HUB_NAME': os.getenv("EVENT_HUB_NAME"),
                'EVENT_HUB_SAS_POLICY': os.getenv("EVENT_HUB_SAS_POLICY"),
                'EVENT_HUB_SAS_KEY': os.getenv("EVENT_HUB_SAS_KEY"),
            }
        }
    }

    ow = OutputWriterFactory.create(config)
    assert ow is not None
    assert isinstance(ow.messaging_client, EventHubStreamingClient)


@pytest.mark.integration
def test_when_configured_event_hub_then_message_sent(mock_listener_client):
    """
    This will test the ability to send message to eventhub.
    We will mock http as it's not being tested.
    :param mock_listener_client:
    :return:
    """

    config = {
        'client': {
            'type': 'eventhub',
            'config': {
                'EVENT_HUB_NAMESPACE': os.getenv("EVENT_HUB_NAMESPACE"),
                'EVENT_HUB_NAME': os.getenv("EVENT_HUB_NAME"),
                'EVENT_HUB_SAS_POLICY': os.getenv("EVENT_HUB_SAS_POLICY"),
                'EVENT_HUB_SAS_KEY': os.getenv("EVENT_HUB_SAS_KEY"),
            }
        }
    }

    ow = OutputWriterFactory.create(config, None, mock_listener_client)
    ow.start_incoming_messages()
    mock_listener_client.mock_new_incoming_message()


@pytest.mark.integration
def test_when_http_configured_then_mesages_are_accepted(mock_streaming_client):
    """
    This will test the ability to accept messages via http.
    We will mock the messaging client.
    :return:
    """

    config = {
        'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
        'OUTPUT_WRITER_HOST': os.getenv("OUTPUT_WRITER_HOST"),
    }

    print('Creating writer')
    ow = OutputWriterFactory.create(config, mock_streaming_client, None)
    print('start_incoming_messages')
    ow.start_incoming_messages()
    # send http
    port = config.get("OUTPUT_WRITER_PORT")
    host = config.get("OUTPUT_WRITER_HOST")
    print('HTTP Post')
    content = json.dumps({'foo': 'bar'}).encode('utf-8')
    requests.post("http://" + host + ":" + port, data=content)

    assert mock_streaming_client.get_sent()
    ow.stop_incoming_messages()


@pytest.mark.integration
def test_when_on_incoming_messages_then_sent_to_event_hub():
    """
    This will test the ability to accept messages via http.
    And then to transport it into event hub.
    :return:
    """

    config = {
        'client': {
            'type': 'eventhub',
            'config': {
                'EVENT_HUB_NAMESPACE': os.getenv("EVENT_HUB_NAMESPACE"),
                'EVENT_HUB_NAME': os.getenv("EVENT_HUB_NAME"),
                'EVENT_HUB_SAS_POLICY': os.getenv("EVENT_HUB_SAS_POLICY"),
                'EVENT_HUB_SAS_KEY': os.getenv("EVENT_HUB_SAS_KEY"),
            }
        },
        'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
        'OUTPUT_WRITER_HOST': os.getenv("OUTPUT_WRITER_HOST"),
    }

    print('Creating writer')
    ow = OutputWriterFactory.create(config)
    print('start_incoming_messages')
    ow.start_incoming_messages()
    # send http
    port = config.get("OUTPUT_WRITER_PORT")
    host = config.get("OUTPUT_WRITER_HOST")
    print('HTTP Post')
    msg = {'foo': 'bar'}
    content = json.dumps(msg).encode('utf-8')
    requests.post("http://" + host + ":" + port, data=content)

    ow.stop_incoming_messages()

    pool = ThreadPool(processes=1)

    async_result = pool.apply_async(get_messages_from_event_hub)
    messages = async_result.get()

    assert len(messages) == 1
    parsed_json = json.loads(messages[0])
    assert msg['foo'] == parsed_json['foo']


def get_messages_from_event_hub():
    receive_config = {
        "AZURE_STORAGE_ACCOUNT": os.getenv("AZURE_STORAGE_ACCOUNT"),
        "AZURE_STORAGE_ACCESS_KEY": os.getenv("AZURE_STORAGE_ACCESS_KEY"),
        "LEASE_CONTAINER_NAME": os.getenv("LEASE_CONTAINER_NAME"),
        "EVENT_HUB_NAMESPACE": os.getenv("EVENT_HUB_NAMESPACE"),
        "EVENT_HUB_NAME": os.getenv("EVENT_HUB_NAME"),
        "EVENT_HUB_SAS_POLICY": os.getenv("EVENT_HUB_SAS_POLICY"),
        "EVENT_HUB_SAS_KEY": os.getenv("EVENT_HUB_SAS_KEY"),
        "EVENT_HUB_CONSUMER_GROUP": os.getenv("EVENT_HUB_CONSUMER_GROUP"),
        "TIMEOUT": 10
    }
    receive_client = EventHubStreamingClient(receive_config)

    global received_messages
    received_messages = []

    def receive_callback(message):
        received_messages.append(message)

    asyncio.set_event_loop(asyncio.new_event_loop())
    receive_client.start_receiving(receive_callback)
    return received_messages
