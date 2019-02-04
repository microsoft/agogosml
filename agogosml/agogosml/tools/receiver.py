#!/usr/bin/env python3
"""Script to receive messages from an agogosml client."""
from argparse import ArgumentParser
from argparse import FileType
from sys import stdout

from agogosml.common.abstract_streaming_client import find_streaming_clients
from agogosml.utils.cli import json_arg


def main(outfile, receiver_class, config):
    """Main entrypoint to the tool."""
    def on_message(message):
        try:
            message = message.decode('utf-8')
        except AttributeError:
            pass

        outfile.write(message.rstrip('\r\n') + '\n')
        return True

    receiver = receiver_class(config)
    receiver.start_receiving(on_message)


def cli():
    """Command-line interface to the tool."""
    streaming_clients = find_streaming_clients()

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--outfile', type=FileType('wb', encoding='utf-8'),
                        default=stdout,
                        help='File to which to write events')
    parser.add_argument('--receiver', choices=sorted(streaming_clients),
                        required=True, default='kafka',
                        help='The receiver to use')
    parser.add_argument('config', type=json_arg,
                        help='JSON configuration passed to the receiver')
    args = parser.parse_args()

    main(args.outfile, streaming_clients[args.receiver], args.config)


if __name__ == '__main__':
    cli()
