import pytest

# from agogosml.common.abstract_streaming_client import AbstractStreamingClient
# from agogosml.common.listener_client import ListenerClient
from agogosml.writer.output_writer import OutputWriter
from .client_mocks import ClientMessagingMock, ListenerClientMock


@pytest.fixture
def MockStreamingClient():
    return ClientMessagingMock()


@pytest.fixture
def MockListenerClient():
    return ListenerClientMock(0)


def test_when_ctor_instance_created(MockStreamingClient, MockListenerClient):
    ow = OutputWriter(MockStreamingClient, MockListenerClient)
    assert ow is not None


def test_on_message_received_sent_called(MockStreamingClient, MockListenerClient):
    ow = OutputWriter(MockStreamingClient, MockListenerClient)
    ow.on_message_received('test')
    assert MockStreamingClient.get_sent()


def test_on_listener_event_sent_called(MockStreamingClient, MockListenerClient):
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
