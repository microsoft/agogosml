"""Abstract streaming client interface."""

from abc import ABC
from abc import abstractmethod
from functools import lru_cache
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Type

from agogosml.utils.imports import find_implementations


class AbstractStreamingClient(ABC):
    """Abstract streaming client interface."""

    @abstractmethod
    def __init__(self, config: dict):
        """Abstract Streaming Client."""
        raise NotImplementedError

    @abstractmethod
    def send(self, message: str) -> bool:
        """Send method."""
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        """Stop method."""
        raise NotImplementedError

    @abstractmethod
    def start_receiving(self, on_message_received_callback: Callable[[str], bool]):
        """Start receiving messages from streaming client."""
        raise NotImplementedError


StreamingClientType = Type[AbstractStreamingClient]


@lru_cache(maxsize=1)
def find_streaming_clients() -> Dict[str, StreamingClientType]:
    """
    Find the friendly-names and constructors of all the streaming clients.

    >>> senders = find_streaming_clients()
    >>> sorted(senders.keys())
    ['broadcast', 'eventhub', 'kafka', 'mock', 'redis', 'storage']
    """
    return {
        client.__name__.replace('StreamingClient', '').lower(): client
        for client in find_implementations(AbstractStreamingClient)
    }


def create_streaming_client_from_config(config: Optional[dict]) -> AbstractStreamingClient:
    """Instantiate a streaming client from configuration."""
    config = config or {}
    try:
        client_config = config['config']
        client_type = config['type']
    except KeyError:
        raise Exception('client cannot be empty')

    try:
        client_class = find_streaming_clients()[client_type]
    except KeyError:
        raise Exception('Unknown client type')

    return client_class(client_config)
