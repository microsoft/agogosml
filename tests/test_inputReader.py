from agogosml.agogosml.streaming_client.abstract_streaming_client import AbstractStreamingClient
from input_reader.input_reader import InputReader

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

def test_when_instance_created():
    cbm = ClientMessagingMock()
    ow = InputReader(cbm)
    assert ow is not None

# async def test_when_send_executing_broker_called():
#     cbm = ClientMessagingMock()
#     assert cbm.receive_called


if __name__ == '__main__':
    test_when_instance_created()