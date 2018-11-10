"""
Main entry point
"""
import os  # temp
from dotenv import load_dotenv  # temp

from output_writer_factory import OutputWriterFactory

load_dotenv()  # temp

if __name__ == "__main__":

    # Setup correct config here
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
                'APP_HOST': os.getenv('APP_HOST'),
                'APP_PORT': os.getenv('APP_PORT')
            },
            'args': {  # NOT SURE WHAT THIS IS FOR.
                'topic': 'testing'
            }}
    }
    OUTPUT = OutputWriterFactory.create(EVENTHUB_CONFIG, None, None)
    OUTPUT.start_incoming_messages()
