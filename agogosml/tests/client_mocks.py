from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.common.listener_client import ListenerClient
from agogosml.common.message_sender import MessageSender


class ClientMessagingMock(AbstractStreamingClient):
    def __init__(self):
        self.sent = False
        self.receiving = False
        self.last_message = None
        pass

    def send(self, msg):
        print(msg)
        self.sent = True
        self.last_message = msg
        pass

    def stop(self, *args, **kwargs):
        pass

    def start_receiving(self, callback):
        self.receiving = True
        self.callback = callback
        pass

    def get_sent(self):
        return self.sent

    def get_last_msg(self):
        return self.last_message

    def get_receiving(self):
        return self.receiving

    def fake_incoming_message_from_streaming(self, msg):
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
