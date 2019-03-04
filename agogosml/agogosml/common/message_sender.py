"""Abstract Message Sender interface."""

from abc import ABC
from abc import abstractmethod


class MessageSender(ABC):
    """Abstract Message Sender interface."""

    @abstractmethod
    def __init__(self, config: dict):
        """Message Sender."""
        raise NotImplementedError

    @abstractmethod
    def send(self, message) -> bool:
        """Send a message."""
        raise NotImplementedError
