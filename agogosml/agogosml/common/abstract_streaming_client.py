"""Abstract streaming client class"""

from abc import ABC, abstractmethod


class AbstractStreamingClient(ABC):
    """
    Abstract Streaming Client
    """
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def send(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def stop(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def start_receiving(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        pass
