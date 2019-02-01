from abc import ABC
from abc import abstractmethod


class MessageSender(ABC):
    @abstractmethod
    def __init__(self, config: dict):
        pass

    @abstractmethod
    def send(self, message) -> bool:
        pass
