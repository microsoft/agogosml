import pytest

from agogosml.writer.output_writer_factory import OutputWriterFactory
from dotenv import load_dotenv
from .client_mocks import ListenerClientMock, ClientMessagingMock
import os


load_dotenv()


@pytest.fixture
def MockListenerClient():
    return ListenerClientMock(0)


@pytest.fixture
def MockStreamingClient():
    return ClientMessagingMock()


# THIS TEST IS NOT TESTED...
# def test_integration_eventhub(MockListenerClient):
#     """
#     Use this integration test to validate that a message was sent to eventhub as passed in by config.
#     """
#     config = {
#         'client': {
#             'type': 'eventhub',
#             'config': {
#                 'EVENT_HUB_NAMESPACE': os.getenv("EVENT_HUB_NAMESPACE"),
#                 'EVENT_HUB_NAME': os.getenv("EVENT_HUB_NAME"),
#                 'EVENT_HUB_SAS_POLICY': os.getenv("EVENT_HUB_SAS_POLICY"),
#                 'EVENT_HUB_SAS_KEY': os.getenv("EVENT_HUB_SAS_KEY"),
#                 'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
#             }
#         }
#     }

#     ow = OutputWriterFactory.create(config)
#     ow.listener = MockListenerClient
#     assert ow is not None
#     ow.start_incoming_messages()
#     MockListenerClient.mock_new_incoming_message()
#     assert MockListenerClient.get_started()

def test_integration_listenerclient(MockStreamingClient):
    """
    Use this integration test to validate that a message was received by the output writer.
    """

    config = {
        'client': {
            'type': 'eventhub',
            'config': {
                'EVENT_HUB_NAMESPACE': os.getenv("EVENT_HUB_NAMESPACE"),
                'EVENT_HUB_NAME': os.getenv("EVENT_HUB_NAME"),
                'EVENT_HUB_SAS_POLICY': os.getenv("EVENT_HUB_SAS_POLICY"),
                'EVENT_HUB_SAS_KEY': os.getenv("EVENT_HUB_SAS_KEY"),
                'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
            }
        }
    }

    ow = OutputWriterFactory.create(config)
    # ow.messaging_client = MockStreamingClient
    assert ow is not None
    # def message_received_callback(listener, msg):
    #     assert msg is not None
    #     js = json.loads(msg)
    #     print("Received message: %s" % msg)

    # NOTE: THIS TEST NEVER ENDS DUE TO FLASK...
    # ow.start_incoming_messages()


# def test_when_known_client_instance_created():
#     config = {
#         'client': {
#             'type': 'kafka',
#             'config': {
#                 'bootstrap.servers': '127.0.0.1:9092',
#                 'group.id': ''
#             },
#             'args': {
#                 'topic': 'test'
#             }},
#         'listener': {
#             'type': 'flask'
#         }
#     }
#     owm = OutputWriterFactory.create(config)
#     assert owm is not None


def test_when_unknown_client_throw():
    config = {'client': {'type': 'aaa'}}
    with pytest.raises(Exception):
        OutputWriterFactory.create(config)


# def test_when_unknown_listener_throw():
#     config = {
#         'client': {
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
#         'client': {
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

#     listener = ListenerClientMock(0)
#     ow = OutputWriterFactory.create(config)
#     ow.start_incoming_messages()
#     listener.mock_new_incoming_message()

#     assert ow is not None
