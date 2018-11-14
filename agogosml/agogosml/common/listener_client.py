"""Abstract listener client broker class"""

from abc import ABC, abstractmethod


class ListenerClient(ABC):

    @abstractmethod
    def __init__(self, port):
        pass

    @abstractmethod
    def start(self, on_message_received):
        pass

    @abstractmethod
    def stop(self):
        pass
