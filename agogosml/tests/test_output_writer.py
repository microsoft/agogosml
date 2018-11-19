import pytest
import os
import asyncio
import requests
from agogosml.writer.output_writer import OutputWriter
from agogosml.writer.output_writer_factory import OutputWriterFactory
from agogosml.common.flask_http_listener_client import FlaskHttpListenerClient
from agogosml.common.kafka_streaming_client import KafkaStreamingClient
from agogosml.common.eventhub_streaming_client import EventHubStreamingClient
from .client_mocks import ClientMessagingMock, ListenerClientMock
import time

@pytest.fixture
def MockStreamingClient():
    return ClientMessagingMock()


@pytest.fixture
def MockListenerClient():
    return ListenerClientMock(0)


def test_when_ctor_instance_created(MockStreamingClient, MockListenerClient):
    ow = OutputWriter(MockStreamingClient, MockListenerClient)
    assert ow is not None


def test_on_message_received_sent_called(MockStreamingClient,
                                         MockListenerClient):
    ow = OutputWriter(MockStreamingClient, MockListenerClient)
    ow.on_message_received('test')
    assert MockStreamingClient.get_sent()


def test_on_listener_event_sent_called(MockStreamingClient,
                                       MockListenerClient):
    ow = OutputWriter(MockStreamingClient, MockListenerClient)
    ow.start_incoming_messages()
    MockListenerClient.mock_new_incoming_message()
    assert MockStreamingClient.get_sent()
    assert MockListenerClient.get_started()


def test_on_stop_event_stop_called(MockStreamingClient, MockListenerClient):
    ow = OutputWriter(MockStreamingClient, MockListenerClient)
    ow.start_incoming_messages()
    ow.stop_incoming_messages()
    assert MockListenerClient.get_stopped()


def test_when_unknown_client_throw():
    config = {'client': {'type': 'aaa'}}
    with pytest.raises(Exception):
        OutputWriterFactory.create(config)


@pytest.mark.integration
def test_output_writer_factory_event_hub():

    config = {
        'client': {
            'type': 'eventhub',
            'config': {
                'EVENT_HUB_NAMESPACE': os.getenv("EVENT_HUB_NAMESPACE"),
                'EVENT_HUB_NAME': os.getenv("EVENT_HUB_NAME"),
                'EVENT_HUB_SAS_POLICY': os.getenv("EVENT_HUB_SAS_POLICY"),
                'EVENT_HUB_SAS_KEY': os.getenv("EVENT_HUB_SAS_KEY"),
                'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
            }
        }
    }

    ow = OutputWriterFactory.create(config)
    assert ow is not None
    assert isinstance(ow.messaging_client, EventHubStreamingClient)
    ow.messaging_client.stop()


@pytest.mark.integration
def test_output_writer_factory_kafka():

    config = {
        'client': {
            'type': 'kafka',
            'config': {
                'KAFKA_TOPIC1': os.getenv("KAFKA_TOPIC"),
                'KAFKA_ADDRESS': os.getenv("KAFKA_ADDRESS"),
                'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
            }
        }
    }

    ow = OutputWriterFactory.create(config)
    assert ow is not None
    assert isinstance(ow.messaging_client, KafkaStreamingClient)
    ow.messaging_client.stop()


#@pytest.mark.integration
def test_output_writer_flask():

    config = {
        'client': {
            'type': 'kafka',
            'config': {
                'KAFKA_TOPIC': os.getenv("KAFKA_TOPIC"),
                'KAFKA_ADDRESS': os.getenv("KAFKA_ADDRESS"),
                'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
                'OUTPUT_WRITER_HOST': os.getenv("OUTPUT_WRITER_HOST"),
            }
        }
    }

    print("whatever")
    ow = OutputWriterFactory.create(config)
    assert ow is not None
    assert isinstance(ow.listener, FlaskHttpListenerClient)

    received_messages = []

    def receive_callback(message):
        received_messages.append(message)

    ow.listener.start(receive_callback)
    time.sleep(10)
    print("stopping server")
    ow.listener.stop()
    
    
