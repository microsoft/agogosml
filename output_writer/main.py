from output_writer.output_writer_factory import OutputWriterFactory

if __name__ == "__main__":

    # TODO: Take from config file, or from URL
    config = {
        'broker': {
            'type': 'kafka',
            'config': {},
            'args': {
                'topic': 'some topic'
            }},
        'listener': {
            'type': 'flask'
        }
    }
    output_writer = OutputWriterFactory.create(config)
    output_writer.start_incoming_messages()
    pass
