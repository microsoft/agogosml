"""Abstract client broker class"""

from abc import ABC, abstractmethod


class AbstractListener(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def start(self, port, message_broker):
        pass

    @abstractmethod
    def stop(self):
        pass
