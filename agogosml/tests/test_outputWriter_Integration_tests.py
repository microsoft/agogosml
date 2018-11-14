import pytest

from agogosml.common.listener_client import ListenerClient
from agogosml.writer.output_writer_factory import OutputWriterFactory


class ListenerClientMock(ListenerClient):

    def __init__(self, port):
        self.callback = None

    def start(self, on_message_received):
        self.callback = on_message_received
        pass

    def stop(self):
        pass

    def mock_new_incoming_message(self):
        self.callback("{'some':'json'}")


def test_when_known_broker_instance_created():
    config = {
        'broker': {
            'type': 'kafka',
            'config': {
                'bootstrap.servers': '127.0.0.1:9092',
                'group.id': ''
            },
            'args': {
                'topic': 'test'
            }},
        'listener': {
            'type': 'flask'
        }
    }
    owm = OutputWriterFactory.create(config)
    assert owm is not None


def test_when_unknown_broker_throw():
    config = {'broker': {'type': 'aaa'}}
    with pytest.raises(Exception):
        OutputWriterFactory.create(config)


# def test_when_unknown_listener_throw():
#     config = {
#         'broker': {
#             'type': 'kafka',
#             'config': {},
#             'args': {
#                 'topic': 'some topic'
#             }},
#         'listener': {
#             'type': 'aaa'
#         }
#     }
#     with pytest.raises(Exception):
#         OutputWriterFactory.create(config)


# def test_integration():
#     config = {
#         'broker': {
#             'type': 'kafka',
#             'config': {
#                 'bootstrap.servers': '127.0.0.1:9092',
#                 'group.id': '',
#                 'topic': 'test'
#             },
#             'args': {
#                 'topic': 'test'
#             }},
#         'listener': {
#             'type': 'flask'
#         }
#     }
#
#     listener = ListenerClientMock(0)
#     ow = OutputWriterFactory.create(config, None, listener)
#     ow.start_incoming_messages()
#     listener.mock_new_incoming_message()
#
#     assert ow is not None
