"""
Main entry point
"""
import os  # temp
from dotenv import load_dotenv  # temp

from agogosml.writer.output_writer_factory import OutputWriterFactory

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
                    'EVENT_HUB_NAMESPACE': os.getenv("EVENT_HUB_NAMESPACE"),
                    'EVENT_HUB_NAME': os.getenv("EVENT_HUB_NAME"),
                    'EVENT_HUB_SAS_POLICY': os.getenv("EVENT_HUB_SAS_POLICY"),
                    'EVENT_HUB_SAS_KEY': os.getenv("EVENT_HUB_SAS_KEY"),
                    'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
                }
            }
        }
    elif msg_type == 'kafka':
        CFG = {
            'broker': {
                'type': 'kafka',
                'config': {
                    'KAFKA_TOPIC': os.getenv("KAFKA_TOPIC"),
                    'KAFKA_ADDRESS': os.getenv("KAFKA_ADDRESS"),
                    'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
                }
            }
        }
    OUTPUT = OutputWriterFactory.create(CFG)
    OUTPUT.start_incoming_messages()
