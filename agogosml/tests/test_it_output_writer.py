import pytest
import os
from dotenv import load_dotenv
from agogosml.writer.output_writer import OutputWriter
from agogosml.writer.output_writer_factory import OutputWriterFactory
from agogosml.common.flask_http_listener_client import FlaskHttpListenerClient
from agogosml.common.kafka_streaming_client import KafkaStreamingClient
from agogosml.common.eventhub_streaming_client import EventHubStreamingClient



def test_when_new_message_then_send_to_event_hub():
    """
    Writer should be able to send message to EventHub
    :return:
    """
    load_dotenv()
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
        },
        'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
        'OUTPUT_WRITER_HOST': os.getenv("OUTPUT_WRITER_HOST"),
    }

    ow = OutputWriterFactory.create(config)
    #ow.start_incoming_messages()
    #ow.on_message_received("{a:123}")
    assert ow is not None
    assert isinstance(ow.messaging_client, EventHubStreamingClient)
    #ow.messaging_client.stop()


@pytest.mark.integration
def test_output_writer_factory_kafka():

    config = {
        'client': {
            'type': 'kafka',
            'config': {
                'KAFKA_TOPIC1': os.getenv("KAFKA_TOPIC"),
                'KAFKA_ADDRESS': os.getenv("KAFKA_ADDRESS"),
                'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
            }
        }
    }

    ow = OutputWriterFactory.create(config)
    assert ow is not None
    assert isinstance(ow.messaging_client, KafkaStreamingClient)
    ow.messaging_client.stop()


@pytest.mark.integration
def test_output_writer_flask():

    config = {
        'client': {
            'type': 'kafka',
            'config': {
                'KAFKA_TOPIC': os.getenv("KAFKA_TOPIC"),
                'KAFKA_ADDRESS': os.getenv("KAFKA_ADDRESS"),
                'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
                'OUTPUT_WRITER_HOST': os.getenv("OUTPUT_WRITER_HOST"),
            }
        }
    }

    ow = OutputWriterFactory.create(config)
    assert ow is not None
    assert isinstance(ow.listener, FlaskHttpListenerClient)

    received_messages = []

    def receive_callback(message):
        received_messages.append(message)

    ow.listener.start(receive_callback)
