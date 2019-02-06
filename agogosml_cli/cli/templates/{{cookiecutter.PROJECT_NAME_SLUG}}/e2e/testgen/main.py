import json
import os
import sys
import time

from agogosml.common.abstract_streaming_client import find_streaming_clients
from agogosml.tools.sender import send
from agogosml.tools.receiver import receive

eh_base_config = {
    "EVENT_HUB_NAMESPACE": os.getenv("EVENT_HUB_NAMESPACE"),
    "EVENT_HUB_NAME": os.getenv("EVENT_HUB_NAME_INPUT"),
    "EVENT_HUB_SAS_POLICY": os.getenv("EVENT_HUB_SAS_POLICY"),
    "EVENT_HUB_SAS_KEY": os.getenv("EVENT_HUB_SAS_KEY_INPUT"),
}

eh_send_config = {
    **eh_base_config,
    'LEASE_CONTAINER_NAME': os.getenv('LEASE_CONTAINER_NAME_INPUT')
}

eh_receive_config = {
    **eh_base_config,
    "AZURE_STORAGE_ACCOUNT": os.getenv("AZURE_STORAGE_ACCOUNT"),
    "AZURE_STORAGE_ACCESS_KEY": os.getenv("AZURE_STORAGE_ACCESS_KEY"),
    "LEASE_CONTAINER_NAME": os.getenv("LEASE_CONTAINER_NAME_OUTPUT"),
    "EVENT_HUB_CONSUMER_GROUP": os.getenv("EVENT_HUB_CONSUMER_GROUP"),
    "TIMEOUT": 10,
    "OUTPUT_TIMEOUT": os.getenv("OUTPUT_TIMEOUT")
}

kafka_base_config = {
    'KAFKA_ADDRESS': os.getenv("KAFKA_ADDRESS"),
    'TIMEOUT': os.getenv('KAFKA_TIMEOUT'),
    # These configs are specific to Event Hub Head for Kafka
    'EVENTHUB_KAFKA_CONNECTION_STRING': os.getenv('EVENTHUB_KAFKA_CONNECTION_STRING'),
    'SSL_CERT_LOCATION': os.getenv('SSL_CERT_LOCATION')  # /usr/local/etc/openssl/cert.pem
}

kafka_receive_config = {
    **kafka_base_config,
    'KAFKA_CONSUMER_GROUP': os.getenv('KAFKA_CONSUMER_GROUP'),
    "OUTPUT_TIMEOUT": os.getenv("OUTPUT_TIMEOUT")
}

kafka_send_config = {
    **kafka_base_config,
    'KAFKA_TOPIC': os.getenv('KAFKA_TOPIC_INPUT')
}


def put_messages_on_input_queue(msg_type: str):
    with open('test_messages.json', encoding='utf-8') as f:
        test_messages = json.load(f)
    send_client = find_streaming_clients()[msg_type]
    send_config = {**eh_send_config, **kafka_send_config}
    send(test_messages, send_client, send_config)


def receive_messages_on_queue(kafka_topic: str, msg_type: str):
    receive_client = find_streaming_clients()[msg_type]
    receive_config = {**eh_receive_config, **kafka_receive_config, **{'KAFKA_TOPIC': os.getenv(kafka_topic)}}
    return receive(sys.stdout, receive_client, receive_config)


def cli():
    msg_type = os.getenv("MESSAGING_TYPE")

    put_messages_on_input_queue(msg_type)

    time.sleep(3)

    input_received = receive_messages_on_queue('KAFKA_TOPIC_INPUT', msg_type)

    print(input_received)

    time.sleep(20)

    output_received = receive_messages_on_queue('KAFKA_TOPIC_OUTPUT', msg_type)

    print(output_received)

    if output_received == "[]":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    cli()
