import asyncio
import time
from multiprocessing.pool import ThreadPool

import os
import json

from agogosml.common.eventhub_streaming_client import EventHubStreamingClient


def send_messages():
    with open('test_messages.json', encoding='utf-8') as f:
        test_messages = json.load(f)

    send_config = {
        "EVENT_HUB_NAMESPACE": os.getenv("EVENT_HUB_NAMESPACE"),
        "EVENT_HUB_NAME": os.getenv("EVENT_HUB_NAME_INPUT"),
        "EVENT_HUB_SAS_POLICY": os.getenv("EVENT_HUB_SAS_POLICY"),
        "EVENT_HUB_SAS_KEY": os.getenv("EVENT_HUB_SAS_KEY_INPUT"),
    }
    send_client = EventHubStreamingClient(send_config)

    for message in test_messages:
        send_client.send(json.dumps(message))

    send_client.stop()
    return json.dumps(test_messages)


def receive_messages():
    pool = ThreadPool(processes=1)

    async_result = pool.apply_async(get_messages_from_event_hub)
    result = async_result.get()

    return json.dumps(result)


def get_messages_from_event_hub():
    receive_config = {
        "AZURE_STORAGE_ACCOUNT": os.getenv("AZURE_STORAGE_ACCOUNT"),
        "AZURE_STORAGE_ACCESS_KEY": os.getenv("AZURE_STORAGE_ACCESS_KEY"),
        "LEASE_CONTAINER_NAME": os.getenv("LEASE_CONTAINER_NAME_OUTPUT"),
        "EVENT_HUB_NAMESPACE": os.getenv("EVENT_HUB_NAMESPACE"),
        "EVENT_HUB_NAME": os.getenv("EVENT_HUB_NAME_OUTPUT"),
        "EVENT_HUB_SAS_POLICY": os.getenv("EVENT_HUB_SAS_POLICY"),
        "EVENT_HUB_SAS_KEY": os.getenv("EVENT_HUB_SAS_KEY_OUTPUT"),
        "EVENT_HUB_CONSUMER_GROUP": os.getenv("EVENT_HUB_CONSUMER_GROUP"),
        "TIMEOUT": 10
    }
    receive_client = EventHubStreamingClient(receive_config)

    global received_messages
    received_messages = []

    def receive_callback(message):
        received_messages.append(message)

    asyncio.set_event_loop(asyncio.new_event_loop())
    receive_client.start_receiving(receive_callback)
    return received_messages


if __name__ == "__main__":
    send = send_messages()
    print(send)
    time.sleep(20)
    receive = receive_messages()
    print(receive)
    if receive == "[]":
        exit(1)
    else:
        exit(0)
