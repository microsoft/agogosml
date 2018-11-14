from agogosml.streaming_client.abstract_streaming_client import AbstractStreamingClient
from agogosml.streaming_client.listener_client import ListenerClient


class ClientMessagingMock(AbstractStreamingClient):
    def __init__(self):
        self.sent = False
        pass

    def send(self, *args, **kwargs):
        self.sent = True
        pass

    def close_send_client(self, *args, **kwargs):
        pass

    def receive(self, *args, **kwargs):
        pass

    def get_sent(self):
        return self.sent


class ListenerClientMock(ListenerClient):
    def __init__(self, port):
        self.callback = None
        self.startCalled = False
        self.stopCalled = False

    def start(self, on_message_received):
        self.callback = on_message_received
        self.startCalled = True
        pass

    def stop(self):
        self.stopCalled = True
        pass

    def mock_new_incoming_message(self):
        self.callback("{'some':'json'}")

    def get_started(self):
        return self.startCalled

    def get_stopped(self):
        return self.stopCalled
