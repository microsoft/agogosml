#!/usr/bin/env python3
"""Script to push inputs to an agogosml client."""
from argparse import ArgumentParser
from argparse import ArgumentTypeError
from argparse import FileType
from sys import stdin
from typing import IO
from typing import Dict
from typing import Tuple

from agogosml.reader.input_reader_factory import StreamingClientType
from agogosml.reader.input_reader_factory import find_streaming_clients


def key_value_arg(value: str) -> Tuple[str, str]:
    """
    >>> key_value_arg('foo=bar')
    ('foo', 'bar')

    >>> key_value_arg('badValue')
    Traceback (most recent call last):
        ...
    argparse.ArgumentTypeError: badValue is not in format key=value
    """
    parts = value.split('=')
    if len(parts) != 2:
        raise ArgumentTypeError('{} is not in format key=value'.format(value))
    return parts[0], parts[1]


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
    parser.add_argument('config', nargs='*', type=key_value_arg,
                        help='Key-value configuration passed to the sender')
    args = parser.parse_args()

    main(args.infile, streaming_clients[args.sender], dict(args.config))


if __name__ == '__main__':
    cli()
