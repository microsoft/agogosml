#!/usr/bin/env python3
"""Script to push inputs to an agogosml client."""
import json
from argparse import ArgumentParser
from argparse import FileType
from sys import stdin

from agogosml.common.abstract_streaming_client import find_streaming_clients
from agogosml.utils.cli import json_arg


def send(messages, sender_class, config):
    """Send messages."""
    sender = sender_class(config)
    for message in messages:
        if not isinstance(message, str):
            message = json.dumps(message)
        sender.send(message.rstrip('\r\n'))
    sender.stop()


def cli():
    """Command-line interface to the tool."""
    streaming_clients = find_streaming_clients()

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--infile', type=FileType('r', encoding='utf-8'),
                        default=stdin,
                        help='File with events to send')
    parser.add_argument('--sender', choices=sorted(streaming_clients),
                        required=True, default='kafka',
                        help='The sender to use')
    parser.add_argument('config', type=json_arg,
                        help='JSON configuration passed to the sender')
    args = parser.parse_args()

    send(args.infile, streaming_clients[args.sender], args.config)


if __name__ == '__main__':
    cli()
