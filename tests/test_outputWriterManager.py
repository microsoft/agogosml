import pytest

from output_writer.output_writer_manager import OutputWriterManager


def test_when_known_broker_instance_created():
    config = {
      'broker': {
        'type': 'kafka',
        'config': {},
        'args': {
          'topic': 'some topic'
        }},
      'listener': {
        'type': 'flask'
      }
    }
    owm = OutputWriterManager(config)
    assert owm is not None


def test_when_unknown_broker_throw():
    config = {'broker': {'type': 'aaa'}}
    with pytest.raises(Exception):
      owm = OutputWriterManager(config)


def test_when_unknown_listener_throw():
    config = {
      'broker': {
        'type': 'kafka',
        'config': {},
        'args': {
          'topic': 'some topic'
        }},
      'listener': {
        'type': 'aaa'
      }
    }
    with pytest.raises(Exception):
      owm = OutputWriterManager(config)


if __name__ == '__main__':
    test_when_known_broker_instance_created()
    test_when_unknown_broker_throw()
    test_when_unknown_listener_throw()
