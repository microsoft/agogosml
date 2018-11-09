"""
Main entry point for input reader
"""
import os  # temp
from dotenv import load_dotenv  # temp

from input_reader_factory import InputReaderFactory

load_dotenv()  # temp

if __name__ == "__main__":

    # FOR NOW, LOAD THE CONFIG VARS IN FROM .ENV
    EVENTHUB_CONFIG = {
        'broker': {
            'type': 'eventhub',
            'config': {
                'AZURE_STORAGE_ACCOUNT': os.getenv("AZURE_STORAGE_ACCOUNT"),
                'AZURE_STORAGE_ACCESS_KEY': os.getenv("AZURE_STORAGE_ACCESS_KEY"),
                'EVENT_HUB_NAMESPACE': os.getenv("EVENT_HUB_NAMESPACE"),
                'EVENT_HUB_NAME': os.getenv("EVENT_HUB_NAME"),
                'EVENT_HUB_SAS_POLICY': os.getenv("EVENT_HUB_SAS_POLICY"),
                'EVENT_HUB_SAS_KEY': os.getenv("EVENT_HUB_SAS_KEY"),
                'LEASE_CONTAINER_NAME' : os.getenv("LEASE_CONTAINER_NAME"),
                'APP_HOST': os.getenv('APP_HOST'),
                'APP_PORT': os.getenv('APP_PORT'),
                'TIMEOUT': 1
            },
            'args': {  # NOT SURE WHAT THIS IS FOR.
                'topic': 'testing'
            }}
    }

    KAFKA_CONFIG = {
        'broker': {
            'type': 'kafka',
            'config': {
                'bootstrap.servers': '127.0.0.1:9092',
                'group.id': 'testgroup',
                'enable.auto.commit': False
            },
            'args': {
                'topic': 'testing'
            }}
    }

    INPUT = InputReaderFactory.create(EVENTHUB_CONFIG)
    INPUT.receive_messages()  # initiate receiving
    print("DONE")

