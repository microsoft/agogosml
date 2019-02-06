"""
Main entry point for output writer
"""
import os

from agogosml.writer.output_writer_factory import OutputWriterFactory

if __name__ == '__main__':

    CFG = {
        'client': {
            'type': os.getenv('MESSAGING_TYPE'),
            'config': os.environ,
        },
        'OUTPUT_WRITER_PORT': os.getenv('OUTPUT_WRITER_PORT'),
        'OUTPUT_WRITER_HOST': os.getenv('OUTPUT_WRITER_HOST'),
    }

    OUTPUT = OutputWriterFactory.create(CFG)
    OUTPUT.start_incoming_messages()
