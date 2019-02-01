from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.common.listener_client import ListenerClient
from agogosml.common.message_sender import MessageSender


class StreamingClientMock(AbstractStreamingClient):
    """
    A class to mock functionality at the streaming client level.
    """
    def __init__(self, config: dict = None):
        self.sent = False
        self.receiving = False
        self.last_message = None
        self.should_fail_to_send = False

    def send(self, msg: str):
        print('Streaming Client Mock send message: %s' % msg)
        if self.should_fail_to_send:
            self.sent = False
            return False
        else:
            self.sent = True
            self.last_message = msg
            return True

    def stop(self):
        pass

    def start_receiving(self, callback):
        self.receiving = True
        self.callback = callback

    def get_sent(self):
        return self.sent

    def get_last_msg(self):
        return self.last_message

    def get_receiving(self):
        return self.receiving

    def fake_incoming_message_from_streaming(self, msg):
        return self.callback(msg)

    def set_fail_send(self, should_fail):
        self.should_fail_to_send = should_fail


class HttpClientMock(ListenerClient):
    """
    A class to mock functionality at the http client level
    """
    def __init__(self, config: dict = None):
        self.callback = None
        self.startCalled = False
        self.stopCalled = False

    def start(self, on_message_received):
        self.callback = on_message_received
        self.startCalled = True

    def stop(self):
        self.stopCalled = True

    def mock_new_incoming_message(self):
        return self.callback("{'some':'json'}")

    def get_started(self):
        return self.startCalled

    def get_stopped(self):
        return self.stopCalled


class MessageSenderMock(MessageSender):
    def __init__(self, config: dict = None):
        self.msg = None
        self.should_fail_to_send = None

    def send(self, msg):
        if self.should_fail_to_send:
            return False
        else:
            self.msg = msg
            return True

    def get_last_msg(self):
        return self.msg

    def set_fail_send(self, should_fail):
        self.should_fail_to_send = should_fail
