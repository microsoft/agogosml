import pytest
import os
from agogosml.common.eventhub_streaming_client import EventHubStreamingClient
from agogosml.common.kafka_streaming_client import KafkaStreamingClient
from agogosml.reader.input_reader import InputReader
from agogosml.reader.input_reader_factory import InputReaderFactory
from .client_mocks import ClientMessagingMock, MessageSenderMock


@pytest.fixture
def MockStreamingClient():
    return ClientMessagingMock()


@pytest.fixture
def MockMessageSender():
    return MessageSenderMock()


def test_when_instance_created(MockStreamingClient, MockMessageSender):
    ir = InputReader(MockStreamingClient, MockMessageSender)
    assert ir is not None


def test_when_start_receiving_then_messaging_client_starts(
        MockStreamingClient, MockMessageSender):
    # arrange
    ir = InputReader(MockStreamingClient, MockMessageSender)

    # act
    ir.start_receiving_messages()
    assert MockStreamingClient.get_receiving()


def test_when_msg_received_callback_called(MockStreamingClient,
                                           MockMessageSender):
    # arrange
    ir = InputReader(MockStreamingClient, MockMessageSender)

    # act
    ir.start_receiving_messages()
    MockStreamingClient.mock_incoming_message_event('a')
    assert MockMessageSender.get_last_msg() == 'a'

# TODO: Try splitting out the unit tests and integration tests into two different directories within tests


@pytest.mark.integration
def test_eventhub_created_from_factory():
    config = {
        'client': {
            'type': 'eventhub',
            'config': {"AZURE_STORAGE_ACCOUNT": os.getenv("AZURE_STORAGE_ACCOUNT"),
                       "AZURE_STORAGE_ACCESS_KEY": os.getenv("AZURE_STORAGE_ACCESS_KEY"),
                       "LEASE_CONTAINER_NAME": os.getenv("LEASE_CONTAINER_NAME"),
                       "EVENT_HUB_NAMESPACE": os.getenv("EVENT_HUB_NAMESPACE"),
                       "EVENT_HUB_NAME": os.getenv("EVENT_HUB_NAME"),
                       "EVENT_HUB_SAS_POLICY": os.getenv("EVENT_HUB_SAS_POLICY"),
                       "EVENT_HUB_SAS_KEY": os.getenv("EVENT_HUB_SAS_KEY"),
                       "EVENT_HUB_CONSUMER_GROUP": os.getenv("EVENT_HUB_CONSUMER_GROUP"),
                       "TIMEOUT": 60
                       }
        }
    }

    ir = InputReaderFactory.create(config)
    assert ir is not None
    assert isinstance(ir, InputReader)
    assert isinstance(ir.messaging_client, EventHubStreamingClient)


@pytest.mark.integration
def test_kafka_created_from_factory():
    config = {
        'client': {
            'type': 'kafka',
            'config': {
                        "KAFKA_TOPIC": os.getenv("KAFKA_TOPIC"),
                        "KAFKA_ADDRESS": os.getenv("KAFKA_ADDRESS"),
                        "KAFKA_CONSUMER_GROUP": os.getenv("KAFKA_CONSUMER_GROUP"),
                        "TIMEOUT": 20
                                }
                            }
                    }
    ir = InputReaderFactory.create(config)
    assert ir is not None
    assert isinstance(ir, InputReader)
    assert isinstance(ir.messaging_client, KafkaStreamingClient)
