import pytest

from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.common.listener_client import ListenerClient
from agogosml.writer.output_writer import OutputWriter


# Can't move to separate file due to errors I can't solve.


class ClientMessagingMock(AbstractStreamingClient):

    def __init__(self):
        self.sent = False
        pass

    def send(self, *args, **kwargs):
        self.sent = True
        pass

    def stop(self, *args, **kwargs):
        pass

    def start_receiving(self, *args, **kwargs):
        pass

    def get_sent(self):
        return self.sent


class ListenerClientMock(ListenerClient):

    def __init__(self, port):
        self.callback = None

    def start(self, on_message_received):
        self.callback = on_message_received
        pass

    def stop(self):
        pass

    def mock_new_incoming_message(self):
        self.callback("{'some':'json'}")


def test_when_ctor_instance_created():
    cbm = ClientMessagingMock()
    clm = ListenerClientMock(0)
    ow = OutputWriter(cbm, clm)
    assert ow is not None


def test_on_message_received_sent_called():
    cbm = ClientMessagingMock()
    clm = ListenerClientMock(0)
    ow = OutputWriter(cbm, clm)
    ow.on_message_received('test')
    assert cbm.get_sent()


def test_on_listener_event_sent_called():
    cbm = ClientMessagingMock()
    clm = ListenerClientMock(0)
    ow = OutputWriter(cbm, clm)
    ow.start_incoming_messages()
    clm.mock_new_incoming_message()
    assert cbm.get_sent()
