"""Abstract listener client broker interface"""

from abc import ABC
from abc import abstractmethod


class ListenerClient(ABC):
    """Abstract listener client broker interface"""

    @abstractmethod
    def __init__(self, config: dict):
        """Abstract listener client broker class"""
        raise NotImplementedError

    @abstractmethod
    def start(self, on_message_received):
        """Start listening"""
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        """Stop listening"""
        raise NotImplementedError
