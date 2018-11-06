from output_writer.output_writer_service_resolver import OutputWriterServiceResolver

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
    owm = OutputWriterServiceResolver(config)
    pass
