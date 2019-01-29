"""Abstract streaming client class"""

from abc import ABC, abstractmethod
from typing import Dict


class AbstractStreamingClient(ABC):
    @abstractmethod
    def __init__(self, config: Dict[str, str]):
        """
        Abstract Streaming Client

        :param config: Dictionary file with all the relevant parameters.
        """
        pass

    @abstractmethod
    def send(self, *args, **kwargs):
        """Send method."""
        pass

    @abstractmethod
    def stop(self, *args, **kwargs):
        """Stop method."""
        pass

    @abstractmethod
    def start_receiving(self, *args, **kwargs):
        """Start receiving messages from streaming client."""
        pass
