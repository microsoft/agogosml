"""
Main entry point for output writer
"""
import os
import time

from agogosml.utils.config import Config
from agogosml.writer.output_writer_factory import OutputWriterFactory

if __name__ == '__main__':
    config = dict(os.environ)
    if 'KAFKA_TOPIC_OUTPUT' in config:
        config['KAFKA_TOPIC'] = config.pop('KAFKA_TOPIC_OUTPUT')

    CFG = {
        'client': {
            'type': os.getenv('MESSAGING_TYPE'),
            'config': Config(config),
        },
        'OUTPUT_WRITER_PORT': os.getenv('OUTPUT_WRITER_PORT'),
        'OUTPUT_WRITER_HOST': os.getenv('OUTPUT_WRITER_HOST'),
    }

    OUTPUT = OutputWriterFactory.create(CFG)
    OUTPUT.start_incoming_messages()
    while True:
        time.sleep(1000)
    print('Finished Receiving Messages')
