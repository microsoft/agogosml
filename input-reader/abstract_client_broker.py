from abc import ABC

class AbstractClientBroker(ABC):
  def __init__():
    pass

  @abstractmethod
  def create_topic(self, topic):
    pass

  @abstractmethod
  def get_producer(self):
    pass

  @abstractmethod
  def get_consumer(self):
    pass

  @abstractmethod
  def mutate_message(self, message:str):
    pass

  @abstractmethod
  async def send(self, message: str):
    if not isinstance(message, str):
      raise TypeError('str type expected for message')

  @abstractmethod
  async def receive(self, message: str):
    if not isinstance(message, str):
      raise TypeError('str type expected for message')

  @instancemethod
  def is_empty(dictionary: dict) -> bool:
    """
    empty dictionaries resolve to false when
    converted to booleans in Python.
    """
    return not bool(dictionary)
