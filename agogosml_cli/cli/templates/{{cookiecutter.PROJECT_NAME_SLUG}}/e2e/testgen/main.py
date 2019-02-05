import asyncio
import json
import os
import sys
import time
from sys import stdout
from multiprocessing.pool import ThreadPool

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
    "TIMEOUT": 10
}

kafka_base_config = {
    'KAFKA_ADDRESS': os.getenv("KAFKA_ADDRESS"),
    'TIMEOUT': os.getenv('TIMEOUT'),
    # These configs are specific to Event Hub Head for Kafka
    'EVENTHUB_KAFKA_CONNECTION_STRING': os.getenv('EVENTHUB_KAFKA_CONNECTION_STRING'),
    'SSL_CERT_LOCATION': os.getenv('SSL_CERT_LOCATION')  # /usr/local/etc/openssl/cert.pem
}

kafka_receive_config = {
    **kafka_base_config,
    'KAFKA_CONSUMER_GROUP': os.getenv('KAFKA_CONSUMER_GROUP'),
    'KAFKA_TOPIC': os.getenv('KAFKA_TOPIC_OUTPUT')
}

kafka_send_config = {
    **kafka_base_config,
    'KAFKA_TOPIC': os.getenv('KAFKA_TOPIC_OUTPUT')
}


def send_messages(msg_type: str):
    with open('test_messages.json', encoding='utf-8') as f:
        test_messages = json.load(f)
    send_client = find_streaming_clients()[msg_type]
    send_config = {**eh_send_config, **kafka_send_config}
    send(test_messages, send_client, send_config)


def receive_messages(msg_type: str):
    # receive messages
    receive_client = find_streaming_clients()[msg_type]
    receive_config = {**eh_receive_config, **kafka_receive_config}
    return receive(stdout, receive_client, receive_config)


def cli():
    msg_type = os.getenv("MESSAGING_TYPE")

    send_messages(msg_type)

    time.sleep(10)

    received = receive_messages(msg_type)

    print(received)

    if received == "[]":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    cli()
