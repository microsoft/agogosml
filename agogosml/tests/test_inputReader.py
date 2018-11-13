import pytest

from agogosml.streaming_client.abstract_streaming_client import AbstractStreamingClient
from agogosml.reader.input_reader import InputReader 
from client_mocks import ClientMessagingMock


@pytest.fixture
def MockStreamingClient():
    return ClientMessagingMock()


def test_when_instance_created(MockStreamingClient):
    ow = InputReader(MockStreamingClient)
    assert ow is not None

# async def test_when_send_executing_broker_called():
#     cbm = ClientMessagingMock()
#     assert cbm.receive_called
