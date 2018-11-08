"""Abstract streaming client class"""

from abc import ABC, abstractmethod


class AbstractStreamingClient(ABC):
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def send(self, *args, **kwargs):
        pass

    @abstractmethod
    def close_send_client(self, *args, **kwargs):
        pass


    @abstractmethod
    def receive(self, *args, **kwargs):
        pass
