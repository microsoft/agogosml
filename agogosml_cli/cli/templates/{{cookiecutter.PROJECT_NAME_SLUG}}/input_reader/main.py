"""
Main entry point for input reader
"""
import os

from agogosml.reader.input_reader_factory import InputReaderFactory
from agogosml.utils.config import Config

if __name__ == "__main__":
    config = dict(os.environ)
    if 'KAFKA_TOPIC_INPUT' in config:
        config['KAFKA_TOPIC'] = config.pop('KAFKA_TOPIC_INPUT')

    CFG = {
        'client': {
            'type': os.getenv("MESSAGING_TYPE"),
            'config': Config(config),
        },
        'APP_HOST': os.getenv('APP_HOST'),
        'APP_PORT': os.getenv('APP_PORT'),
    }

    INPUT = InputReaderFactory.create(CFG)
    INPUT.start_receiving_messages()  # initiate receiving
    print("DONE")
