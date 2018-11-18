from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.common.listener_client import ListenerClient
from agogosml.common.message_sender import MessageSender


class ClientMessagingMock(AbstractStreamingClient):
    def __init__(self):
        self.sent = False
        self.receving = False
        pass

    def send(self, *args, **kwargs):
        self.sent = True
        pass

    def stop(self, *args, **kwargs):
        pass

    def start_receiving(self, callback):
        self.receving = True
        self.callback = callback
        pass

    def get_sent(self):
        return self.sent

    def get_receiving(self):
        return self.receving

    def mock_incoming_message_event(self, msg):
        self.callback(msg)


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


class MessageSenderMock(MessageSender):
    def __init__(self):
        pass

    def send(self, msg):
        self.msg = msg
        pass

    def get_last_msg(self):
        return self.msg
