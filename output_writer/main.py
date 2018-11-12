"""
Main entry point
"""
import os  # temp
from dotenv import load_dotenv  # temp

from output_writer_factory import OutputWriterFactory

load_dotenv()  # temp

if __name__ == "__main__":

    msg_type = os.getenv("MESSAGING_TYPE")
    CFG = None

    if msg_type == 'eventhub':
        # FOR NOW, LOAD THE CONFIG VARS IN FROM .ENV
        CFG = {
            'broker': {
                'type': 'eventhub',
                'config': {
                    'AZURE_STORAGE_ACCOUNT': os.getenv("AZURE_STORAGE_ACCOUNT"),
                    'AZURE_STORAGE_ACCESS_KEY': os.getenv("AZURE_STORAGE_ACCESS_KEY"),
                    'EVENT_HUB_NAMESPACE': os.getenv("EVENT_HUB_NAMESPACE"),
                    'EVENT_HUB_NAME': os.getenv("EVENT_HUB_NAME"),
                    'EVENT_HUB_SAS_POLICY': os.getenv("EVENT_HUB_SAS_POLICY"),
                    'EVENT_HUB_SAS_KEY': os.getenv("EVENT_HUB_SAS_KEY"),
                    'LEASE_CONTAINER_NAME': os.getenv("LEASE_CONTAINER_NAME"),
                    'APP_HOST': os.getenv('APP_HOST'),
                    'APP_PORT': os.getenv('APP_PORT'),
                    'TIMEOUT': 1
                }
            }
        }
    elif msg_type == 'kafka':
        CFG = {
            'broker': {
                'type': 'kafka',
                'config': {
                    'KAFKA_TOPIC': os.getenv("KAFKA_TOPIC"),
                    'KAFKA_CONSUMER_GROUP': os.getenv("KAFKA_CONSUMER_GROUP"),
                    'APP_HOST': os.getenv("APP_HOST"),
                    'APP_PORT': os.getenv("APP_PORT"),
                    'KAFKA_ADDRESS': os.getenv("APP_PORT"),

                }
            }
        }
    OUTPUT = OutputWriterFactory.create(CFG, None, None)
    OUTPUT.start_incoming_messages()
