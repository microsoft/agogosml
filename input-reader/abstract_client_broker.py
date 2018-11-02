"""Abstract client broker class"""

from abc import ABC, abstractmethod


class AbstractClientBroker(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_topic(self, topic):
        pass

    @abstractmethod
    def get_producer(self):
        pass

    @abstractmethod
    def get_consumer(self):
        pass

    @abstractmethod
    def mutate_message(self, message: str):
        pass

    @abstractmethod
    async def send(self, message: str):
        if not isinstance(message, str):
            raise TypeError('str type expected for message')

    @abstractmethod
    async def receive(self, message: str):
        if not isinstance(message, str):
            raise TypeError('str type expected for message')
