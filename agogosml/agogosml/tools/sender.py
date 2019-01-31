#!/usr/bin/env python3
"""Script to push inputs to an agogosml client."""
from argparse import ArgumentParser
from argparse import ArgumentTypeError
from argparse import FileType
from json import loads
from sys import stdin
from typing import IO
from typing import Dict

from agogosml.common.abstract_streaming_client import StreamingClientType
from agogosml.common.abstract_streaming_client import find_streaming_clients


def json_arg(value: str):
    """
    >>> json_arg('{"foo": "bar", "baz": [1, 2]}')
    {'foo': 'bar', 'baz': [1, 2]}

    >>> json_arg('{')
    Traceback (most recent call last):
        ...
    argparse.ArgumentTypeError: { is not in JSON format
    """
    try:
        return loads(value)
    except ValueError:
        raise ArgumentTypeError('%s is not in JSON format' % value)


def main(messages: IO[str], sender_class: StreamingClientType, config: Dict[str, str]):
    sender = sender_class(config)
    for message in messages:
        sender.send(message.rstrip('\r\n'))


def cli():
    streaming_clients = find_streaming_clients()

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--infile', type=FileType('r', encoding='utf-8'),
                        required=True, default=stdin,
                        help='File with events to send')
    parser.add_argument('--sender', choices=sorted(streaming_clients),
                        required=True, default='kafka',
                        help='The sender to use')
    parser.add_argument('config', type=json_arg,
                        help='JSON configuration passed to the sender')
    args = parser.parse_args()

    main(args.infile, streaming_clients[args.sender], args.config)


if __name__ == '__main__':
    cli()
