"""
Main entry point for input reader
"""
import os

from agogosml.reader.input_reader_factory import InputReaderFactory
from agogosml.utils.config import Config

if __name__ == "__main__":

    CFG = {
        'client': {
            'type': os.getenv("MESSAGING_TYPE"),
            'config': Config(os.environ),
        },
        'APP_HOST': os.getenv('APP_HOST'),
        'APP_PORT': os.getenv('APP_PORT'),
    }

    INPUT = InputReaderFactory.create(CFG)
    INPUT.start_receiving_messages()  # initiate receiving
    print("DONE")
