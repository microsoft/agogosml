import pytest
import os
from agogosml.common.eventhub_streaming_client import EventHubStreamingClient
from agogosml.common.kafka_streaming_client import KafkaStreamingClient
from agogosml.reader.input_reader import InputReader
from agogosml.reader.input_reader_factory import InputReaderFactory
from .client_mocks import StreamingClientMock, MessageSenderMock


@pytest.fixture
def mock_streaming_client():
    return StreamingClientMock()


@pytest.fixture
def mock_message_sender():
    return MessageSenderMock()


def test_when_instance_created(mock_streaming_client, mock_message_sender):
    ir = InputReader(mock_streaming_client, mock_message_sender)
    assert ir is not None


def test_when_start_receiving_then_messaging_client_starts(mock_streaming_client, mock_message_sender):
    # arrange
    ir = InputReader(mock_streaming_client, mock_message_sender)

    # act
    ir.start_receiving_messages()
    assert mock_streaming_client.get_receiving()


def test_when_msg_received_callback_called(mock_streaming_client,
                                           mock_message_sender):
    # arrange
    ir = InputReader(mock_streaming_client, mock_message_sender)

    # act
    ir.start_receiving_messages()
    mock_streaming_client.fake_incoming_message_from_streaming('a')
    assert mock_message_sender.get_last_msg() == 'a'


def test_when_failed_to_deliver_then_failure_callback(mock_streaming_client, mock_message_sender):
    # arrange
    ir = InputReader(mock_streaming_client, mock_message_sender)

    # act
    ir.start_receiving_messages()
    mock_message_sender.set_fail_send(True)
    result = mock_streaming_client.fake_incoming_message_from_streaming('a')

    # assert
    assert result is False


# TODO: Try splitting out the unit tests and integration tests into two different directories within tests


@pytest.mark.integration
def test_eventhub_created_from_factory():
    config = {
        'client': {
            'type': 'eventhub',
            'config': {
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
        },
        "APP_HOST": os.getenv("APP_HOST"),
        "APP_PORT": os.getenv("APP_PORT")
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
                "KAFKA_TOPIC": os.getenv("KAFKA_TOPIC_INPUT"),
                "KAFKA_ADDRESS": os.getenv("KAFKA_ADDRESS"),
                "KAFKA_CONSUMER_GROUP": os.getenv("KAFKA_CONSUMER_GROUP"),
                "TIMEOUT": 20,
                'EVENTHUB_KAFKA_CONNECTION_STRING': os.getenv('EVENTHUB_KAFKA_CONNECTION_STRING')
            }
        },
        "APP_HOST": os.getenv("APP_HOST"),
        "APP_PORT": os.getenv("APP_PORT")
    }
    ir = InputReaderFactory.create(config)
    assert ir is not None
    assert isinstance(ir, InputReader)
    assert isinstance(ir.messaging_client, KafkaStreamingClient)
