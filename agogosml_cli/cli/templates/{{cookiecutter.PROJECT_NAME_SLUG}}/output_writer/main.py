"""
Main entry point for output writer
"""
import os

from agogosml.writer.output_writer_factory import OutputWriterFactory

if __name__ == "__main__":

    msg_type = os.getenv("MESSAGING_TYPE")
    CFG = None

    if msg_type == 'eventhub':
        CFG = {
            'client': {
                'type': 'eventhub',
                'config': {
                    'EVENT_HUB_NAMESPACE': os.getenv("EVENT_HUB_NAMESPACE"),
                    'EVENT_HUB_NAME': os.getenv("EVENT_HUB_NAME"),
                    'EVENT_HUB_SAS_POLICY': os.getenv("EVENT_HUB_SAS_POLICY"),
                    'EVENT_HUB_SAS_KEY': os.getenv("EVENT_HUB_SAS_KEY"),
                    'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
                    'OUTPUT_WRITER_HOST': os.getenv("OUTPUT_WRITER_HOST"),
                }
            }
        }
    elif msg_type == 'kafka':
        CFG = {
            'client': {
                'type': 'kafka',
                'config': {
                    'KAFKA_TOPIC': os.getenv("KAFKA_TOPIC"),
                    'KAFKA_ADDRESS': os.getenv("KAFKA_ADDRESS"),
                    'OUTPUT_WRITER_PORT': os.getenv("OUTPUT_WRITER_PORT"),
                    'OUTPUT_WRITER_HOST': os.getenv("OUTPUT_WRITER_HOST"),
                }
            }
        }
    OUTPUT = OutputWriterFactory.create(CFG)
    OUTPUT.start_incoming_messages()
