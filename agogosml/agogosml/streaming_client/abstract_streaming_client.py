"""Abstract streaming client class"""

from abc import ABC, abstractmethod


class AbstractStreamingClient(ABC):
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    async def send(self):
        pass

    @abstractmethod
    async def receive(self, *args, **kwargs):
        pass
