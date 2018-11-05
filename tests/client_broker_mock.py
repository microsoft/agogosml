from io_base.abstract_client_broker import AbstractClientBroker


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



