from io_base.abstract_client_broker import AbstractClientBroker


class OutputWriter:
    def __init__(self, client_broker: AbstractClientBroker):
        self.clientBroker = client_broker
        pass

    async def send(self, message: str):
        await self.clientBroker.send(message)
        pass
