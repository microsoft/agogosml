"""
Main entry point for input reader
"""
import os

from agogosml.reader.input_reader_factory import InputReaderFactory

if __name__ == "__main__":

    msg_type = os.getenv("MESSAGING_TYPE")
    CFG = None

    if msg_type == 'eventhub':
        # FOR NOW, LOAD THE CONFIG VARS IN FROM .ENV
        CFG = {
            'client': {
                'type': 'eventhub',
                'config': {
                    'AZURE_STORAGE_ACCOUNT':
                    os.getenv("AZURE_STORAGE_ACCOUNT"),
                    'AZURE_STORAGE_ACCESS_KEY':
                    os.getenv("AZURE_STORAGE_ACCESS_KEY"),
                    'EVENT_HUB_NAMESPACE':
                    os.getenv("EVENT_HUB_NAMESPACE"),
                    'EVENT_HUB_NAME':
                    os.getenv("EVENT_HUB_NAME"),
                    'EVENT_HUB_SAS_POLICY':
                    os.getenv("EVENT_HUB_SAS_POLICY"),
                    'EVENT_HUB_SAS_KEY':
                    os.getenv("EVENT_HUB_SAS_KEY"),
                    'LEASE_CONTAINER_NAME':
                    os.getenv("LEASE_CONTAINER_NAME"),
                    'APP_HOST':
                    os.getenv('APP_HOST'),
                    'APP_PORT':
                    os.getenv('APP_PORT'),
                    'TIMEOUT':
                    os.getenv('TIMEOUT')
                }
            }
        }
    elif msg_type == 'kafka':
        CFG = {
            'client': {
                'type': 'kafka',
                'config': {
                    'KAFKA_TOPIC': os.getenv("KAFKA_TOPIC"),
                    'KAFKA_CONSUMER_GROUP': os.getenv("KAFKA_CONSUMER_GROUP"),
                    'APP_HOST': os.getenv("APP_HOST"),
                    'APP_PORT': os.getenv("APP_PORT"),
                    'KAFKA_ADDRESS': os.getenv("KAFKA_ADDRESS"),
                    'TIMEOUT': os.getenv('TIMEOUT')
                }
            }
        }

    INPUT = InputReaderFactory.create(CFG)
    INPUT.start_receiving_messages()  # initiate receiving
    print("DONE")
