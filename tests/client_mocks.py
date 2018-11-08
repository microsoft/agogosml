from agogosml.agogosml.streaming_client import AbstractStreamingClient
from agogosml.agogosml.streaming_client.listener_client import ListenerClient


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

    def start(self, on_message_received):
        self.callback = on_message_received
        pass

    def stop(self):
        pass

    def mock_new_incoming_message(self):
        self.callback("{'some':'json'}")