"""
Main entry point
"""
from output_writer.output_writer_factory import OutputWriterFactory

if __name__ == "__main__":

    # Setup correct config here
    CONFIG = {
    }
    OUTPUT = OutputWriterFactory.create(CONFIG, None, None)
    OUTPUT.start_incoming_messages()