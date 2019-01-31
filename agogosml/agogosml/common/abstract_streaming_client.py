"""Abstract streaming client class"""

from abc import ABC
from abc import abstractmethod
from functools import lru_cache
from typing import Dict
from typing import Type

from agogosml.utils.imports import find_implementations


class AbstractStreamingClient(ABC):
    @abstractmethod
    def __init__(self, config: dict):
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


StreamingClientType = Type[AbstractStreamingClient]


@lru_cache(maxsize=1)
def find_streaming_clients() -> Dict[str, StreamingClientType]:
    """
    >>> senders = find_streaming_clients()
    >>> sorted(senders.keys())
    ['broadcast', 'eventhub', 'kafka', 'mock']
    """
    return {
        client.__name__.replace('StreamingClient', '').lower(): client
        for client in find_implementations(AbstractStreamingClient)
    }


def create_streaming_client_from_config(config: dict) -> AbstractStreamingClient:
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
