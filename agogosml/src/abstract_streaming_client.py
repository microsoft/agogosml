"""Abstract streaming client class"""

from abc import ABC, abstractmethod


class KafkaClientBroker(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def mutate_message(self, message: str):
        pass

    @abstractmethod
    def get_producer(self):
        pass

    @abstractmethod
    def get_consumer(self):
        pass
    
    @abstractmethod
    async def send(self):
        pass

    @abstractmethod
    async def receive(self, *args, **kwargs):
        pass

