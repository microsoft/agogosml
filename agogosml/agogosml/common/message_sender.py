"""Abstract Message Sender class"""

from abc import ABC
from abc import abstractmethod


class MessageSender(ABC):
    @abstractmethod
    def __init__(self, config: dict):
        """Message Sender."""
        pass

    @abstractmethod
    def send(self, message) -> bool:
        """Sends message."""
        pass
