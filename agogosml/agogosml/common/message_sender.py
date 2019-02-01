"""Abstract Message Sender class"""

from abc import ABC
from abc import abstractmethod


class MessageSender(ABC):
    """Message Sender class."""

    @abstractmethod
    def __init__(self, config: dict):
        pass

    @abstractmethod
    def send(self, *args, **kwargs):
        """
        Sends message.
        """
        pass
