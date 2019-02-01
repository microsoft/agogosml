"""Abstract listener client broker class"""

from abc import ABC
from abc import abstractmethod


class ListenerClient(ABC):
    @abstractmethod
    def __init__(self, config: dict):
        """Abstract listener client broker class"""
        pass

    @abstractmethod
    def start(self, on_message_received):
        """Start listening"""
        pass

    @abstractmethod
    def stop(self):
        """Stop listening"""
        pass
