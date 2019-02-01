from abc import ABC
from abc import abstractmethod
from typing import Callable

Callback = Callable[[str], bool]


class ListenerClient(ABC):

    @abstractmethod
    def __init__(self, config: dict):
        pass

    @abstractmethod
    def start(self, on_message_received: Callback):
        pass

    @abstractmethod
    def stop(self):
        pass
