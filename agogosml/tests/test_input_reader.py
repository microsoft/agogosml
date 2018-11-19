import pytest

# from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.reader.input_reader import InputReader
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


def test_when_start_receiving_then_messaging_client_starts(MockStreamingClient, MockMessageSender):
    # arrange
    ir = InputReader(MockStreamingClient, MockMessageSender)

    # act
    ir.start_receiving_messages()
    assert MockStreamingClient.get_receiving()


def test_when_msg_received_callback_called(MockStreamingClient, MockMessageSender):
    # arrange
    ir = InputReader(MockStreamingClient, MockMessageSender)

    # act
    ir.start_receiving_messages()
    MockStreamingClient.mock_incoming_message_event('a')
    assert MockMessageSender.get_last_msg() == 'a'
