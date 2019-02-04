import asyncio
import json
import os
import time
from multiprocessing.pool import ThreadPool

from agogosml.common.eventhub_streaming_client import EventHubStreamingClient
from agogosml.common.kafka_streaming_client import KafkaStreamingClient

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
    'SSL_CERT_LOCATION': os.getenv('SSL_CERT_LOCATION')
}

kafka_receive_config = {
    **kafka_base_config,
    'KAFKA_CONSUMER_GROUP': os.getenv('KAFKA_CONSUMER_GROUP'),
    'KAFKA_TOPIC_INPUT': os.getenv('KAFKA_TOPIC_INPUT')
}

kafka_send_config = {
    **kafka_base_config,
    'KAFKA_TOPIC_OUTPUT': os.getenv('KAFKA_TOPIC_OUTPUT')
}


def receive_messages(msg_type: str):
    pool = ThreadPool(processes=1)

    async_result = pool.apply_async(get_messages_from_client, args=(msg_type,))

    result = async_result.get()

    return json.dumps(result)


def send_messages_to_client(msg_type: str):
    with open('test_messages.json', encoding='utf-8') as f:
        test_messages = json.load(f)

    send_client = EventHubStreamingClient(eh_send_config) if msg_type == 'eventhub' \
        else KafkaStreamingClient(kafka_send_config)

    for message in test_messages:
        send_client.send(json.dumps(message))

    send_client.stop()
    return json.dumps(test_messages)


def get_messages_from_client(msg_type: str):
    receive_client = EventHubStreamingClient(eh_receive_config) if msg_type == 'eventhub' \
        else KafkaStreamingClient(kafka_receive_config)

    global received_messages
    received_messages = []

    def receive_callback(message):
        received_messages.append(message)

    asyncio.set_event_loop(asyncio.new_event_loop())
    receive_client.start_receiving(receive_callback)
    return received_messages


if __name__ == "__main__":
    msg_type = os.getenv("MESSAGING_TYPE")
    send = send_messages_to_client(msg_type)
    print(send)
    time.sleep(20)
    receive = receive_messages(msg_type)
    print(receive)
    if receive == "[]":
        exit(1)
    else:
        exit(0)
