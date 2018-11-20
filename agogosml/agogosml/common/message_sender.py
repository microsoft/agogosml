"""Abstract Message Sender class"""

from abc import ABC, abstractmethod


class MessageSender(ABC):  # pylint: disable=too-few-public-methods
    """Message Sender class."""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def send(self, *args, **kwargs):
        """
        Sends message.
        """
        pass
