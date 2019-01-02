import datetime
import threading

import pytest
import os
import time
from dotenv import load_dotenv

from agogosml.common.kafka_streaming_client import KafkaStreamingClient
from agogosml.reader.input_reader_factory import InputReaderFactory
from agogosml.writer.output_writer_factory import OutputWriterFactory
from tests.client_mocks import StreamingClientMock, HttpClientMock
from tests.integration_tests.test_app import TestApp

load_dotenv()


@pytest.fixture
def mock_streaming_client():
    return StreamingClientMock()


@pytest.fixture
def mock_listener_client():
    return HttpClientMock(0)


@pytest.mark.integration
def test_when_messages_received_in_input_then_all_messages_are_sent_via_output():
    """
    This function tests the integration of input and output.
    It assumes connectivity to streaming client is correct, therefore the steaming client is mocked.
    We look to find that once a message is received, it is send out by the output writer.
    This is the maximal integration test we can have in an isolated environment.
    :return:
    """

    # setup input
    input_client_mock = StreamingClientMock()
    ir_config = {
        'APP_PORT': os.getenv("APP_PORT"),
        'APP_HOST': os.getenv("APP_HOST"),
    }
    print('Creating reader')
    ir = InputReaderFactory.create(ir_config, input_client_mock)
    print('start_receiving_messages')
    ir.start_receiving_messages()

    # setup app
    app = TestApp(os.getenv("APP_PORT"),
                  os.getenv("APP_HOST"),
                  os.getenv("OUTPUT_WRITER_PORT"),
                  os.getenv("OUTPUT_WRITER_HOST"))
    app.start()

    # setup output
    ow_config = {
        'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
        'OUTPUT_WRITER_HOST': os.getenv("OUTPUT_WRITER_HOST"),
    }

    print('Creating writer')
    output_client_mock = StreamingClientMock()
    ow = OutputWriterFactory.create(ow_config, output_client_mock, None)
    print('start_incoming_messages')
    ow.start_incoming_messages()

    print('sending test message to reader')
    test_msg = str(time.clock())
    # send a message from INPUT reader, and expect it to flow in the pipeline,
    # and eventually be picked up by the output writer
    input_client_mock.fake_incoming_message_from_streaming(test_msg)
    last_msg = output_client_mock.get_last_msg()

    assert last_msg == test_msg
    ir.stop_incoming_messages()
    ow.stop_incoming_messages()


@pytest.mark.integration
def test_when_error_in_output_then_pipeline_fails():
    """
    This function tests the integration of input and output.
    It assumes connectivity to streaming client is correct, therefore the steaming client is mocked.
    We look to find that once a message is received, it is send out by the output writer.
    This is the maximal integration test we can have in an isolated environment.
    :return:
    """

    # setup input
    input_client_mock = StreamingClientMock()
    ir_config = {
        'APP_PORT': os.getenv("APP_PORT"),
        'APP_HOST': os.getenv("APP_HOST"),
    }
    print('Creating reader')
    ir = InputReaderFactory.create(ir_config, input_client_mock)
    print('start_receiving_messages')
    ir.start_receiving_messages()

    # setup app
    app = TestApp(os.getenv("APP_PORT"),
                  os.getenv("APP_HOST"),
                  os.getenv("OUTPUT_WRITER_PORT"),
                  os.getenv("OUTPUT_WRITER_HOST"))
    app.start()

    # setup output
    ow_config = {
        'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
        'OUTPUT_WRITER_HOST': os.getenv("OUTPUT_WRITER_HOST"),
    }

    print('Creating writer')
    output_client_mock = StreamingClientMock()
    ow = OutputWriterFactory.create(ow_config, output_client_mock, None)
    print('start_incoming_messages')

    # Set to fail on Output Send:
    output_client_mock.set_fail_send(True)
    print('sending test message to reader')
    test_msg = str(time.clock())
    # send a message from INPUT reader, and expect it to flow in the pipeline,
    # and eventually be picked up by the output writer
    result = input_client_mock.fake_incoming_message_from_streaming(test_msg)
    last_msg = output_client_mock.get_last_msg()

    assert last_msg is None
    assert result is False
    ir.stop_incoming_messages()
    ow.stop_incoming_messages()


@pytest.mark.integration
def test_when_messages_sent_to_kafka_then_all_messages_are_sent_via_output():
    """
    This function tests the integration of input and output.
    It assumes connectivity to streaming client is correct, therefore the steaming client is mocked.
    We look to find that once a message is received, it is send out by the output writer.
    This is the maximal integration test we can have in an isolated environment.
    Please allow KAFKA_TIMEOUT of 30 seconds or more
    :return:
    """

    # setup input

    ir_config = {
        'client': {
            'type': 'kafka',
            'config': {
                "KAFKA_TOPIC": os.getenv("KAFKA_TOPIC_INPUT"),
                "KAFKA_ADDRESS": os.getenv("KAFKA_ADDRESS"),
                "KAFKA_CONSUMER_GROUP": os.getenv("KAFKA_CONSUMER_GROUP"),
                "TIMEOUT": os.getenv("KAFKA_TIMEOUT")
            }
        },
        'APP_PORT': os.getenv("APP_PORT"),
        'APP_HOST': os.getenv("APP_HOST"),
    }
    print('Creating reader')
    ir = InputReaderFactory.create(ir_config)

    # setup app
    app = TestApp(os.getenv("APP_PORT"),
                  os.getenv("APP_HOST"),
                  os.getenv("OUTPUT_WRITER_PORT"),
                  os.getenv("OUTPUT_WRITER_HOST"))
    app.start()

    # setup output
    ow_config = {
        'client': {
            'type': 'kafka',
            'config': {
                "KAFKA_TOPIC": os.getenv("KAFKA_TOPIC_OUTPUT"),
                "KAFKA_ADDRESS": os.getenv("KAFKA_ADDRESS"),
                "TIMEOUT": os.getenv("KAFKA_TIMEOUT")
            }
        },
        'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
        'OUTPUT_WRITER_HOST': os.getenv("OUTPUT_WRITER_HOST"),
    }

    print('Creating writer')
    ow = OutputWriterFactory.create(ow_config, None, None)
    print('start_incoming_messages')
    ow.start_incoming_messages()

    print('start_receiving_messages')
    # ir.start_receiving_messages()
    t_ir = threading.Thread(name='testir', target=ir.start_receiving_messages)
    t_ir.setDaemon(True)
    t_ir.start()

    print('sending test message to reader')

    test_msg = str(time.clock())
    print("sending {} to input topic".format(test_msg))
    # send a message from INPUT reader, and expect it to flow in the pipeline,
    # and eventually be picked up by the output writer
    send_message_to_kafka(test_msg)
    last_msg = read_message_from_kafka()
    print("received {} from output topic".format(last_msg))
    assert last_msg == test_msg

    ir.stop_incoming_messages()
    ow.stop_incoming_messages()


def send_message_to_kafka(msg):
    config = {
        "KAFKA_TOPIC": os.getenv("KAFKA_TOPIC_INPUT"),
        "KAFKA_ADDRESS": os.getenv("KAFKA_ADDRESS"),
        "TIMEOUT": os.getenv("KAFKA_TIMEOUT")
    }
    kafka = KafkaStreamingClient(config)
    val = kafka.send(msg)
    return val


def read_message_from_kafka():
    config = {
        "KAFKA_TOPIC": os.getenv("KAFKA_TOPIC_OUTPUT"),
        "KAFKA_ADDRESS": os.getenv("KAFKA_ADDRESS"),
        "KAFKA_CONSUMER_GROUP": os.getenv("KAFKA_CONSUMER_GROUP"),
        "TIMEOUT": os.getenv("KAFKA_TIMEOUT")
    }
    kafka = KafkaStreamingClient(config)
    kafka.start_receiving(on_msg)

    start = datetime.datetime.now()
    timeout = int(os.getenv("KAFKA_TIMEOUT"))
    stop = False
    msg = None
    while not stop:
        # Stop loop after timeout if exists
        elapsed = datetime.datetime.now() - start
        if elapsed.seconds >= timeout:
            stop = True

        # Poll messages from topic
        if my_msg is not None:
            stop = True
            msg = my_msg

    return msg


my_msg = None


def on_msg(msg):
    global my_msg
    my_msg = msg.decode('utf-8')

