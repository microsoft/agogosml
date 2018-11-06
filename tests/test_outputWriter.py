from io_base.abstract_client_broker import AbstractClientBroker
from output_writer.output_writer import OutputWriter

# Can't move to separate file due to errors I can't solve.
class ClientBrokerMock(AbstractClientBroker):
    def __init__(self):
      self.send_called = False
      pass

    def create_topic(self, topic):
      pass

    def mutate_message(self, message: str):
      pass

    async def send(self, message: str):
      self.send_called = True
      pass

    async def receive(self, message: str):
      pass


def test_when_ctor_instance_created():
    cbm = ClientBrokerMock()
    ow = OutputWriter(cbm)
    assert ow is not None


async def test_when_send_executing_broker_called():
    cbm = ClientBrokerMock()
    ow = OutputWriter(cbm)
    await ow.send('test')
    assert cbm.send_called


if __name__ == '__main__':
    test_when_ctor_instance_created()
    test_when_send_executing_broker_called()
    pass
