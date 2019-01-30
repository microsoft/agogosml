#!/usr/bin/env python3
"""Script to push inputs to an agogosml client."""
from argparse import ArgumentParser
from argparse import ArgumentTypeError
from argparse import FileType
from importlib import import_module
from inspect import getsourcefile
from pathlib import Path
from pkgutil import walk_packages
from sys import stdin
from typing import Dict
from typing import IO
from typing import Iterable
from typing import Tuple
from typing import Type
from typing import TypeVar

from agogosml.common.abstract_streaming_client import AbstractStreamingClient

T = TypeVar('T')
SenderType = Type[AbstractStreamingClient]


def get_base_module(interface) -> Tuple[str, Path]:
    base_module_name = '.'.join(interface.__module__.split('.')[:-1])
    base_module_path = Path(getsourcefile(interface)).parent
    return base_module_name, base_module_path


def import_subpackages(module_prefix: str, module_path: Path):
    for _, module, _ in walk_packages([str(module_path)]):
        sub_module_name = '{}.{}'.format(module_prefix, module)
        import_module(sub_module_name)


def find_implementations(interface: Type[T]) -> Iterable[Type[T]]:
    base_module_name, base_module_path = get_base_module(interface)
    import_subpackages(base_module_name, base_module_path)
    return interface.__subclasses__()


def find_senders() -> Dict[str, SenderType]:
    """
    >>> senders = find_senders()
    >>> sorted(senders.keys())
    ['eventhub', 'kafka', 'mock']
    """
    return {
        client.__name__.replace('StreamingClient', '').lower(): client
        for client in find_implementations(AbstractStreamingClient)
    }


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


def main(messages: IO[str], sender_class: SenderType, config: Dict[str, str]):
    sender = sender_class(config)
    for message in messages:
        sender.send(message.rstrip('\r\n'))


def cli():
    senders = find_senders()

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--infile', type=FileType('r', encoding='utf-8'),
                        required=True, default=stdin,
                        help='File with events to send')
    parser.add_argument('--sender', choices=sorted(senders),
                        required=True, default='kafka',
                        help='The sender to use')
    parser.add_argument('config', nargs='*', type=key_value_arg,
                        help='Key-value configuration passed to the sender')
    args = parser.parse_args()

    main(args.infile, senders[args.sender], dict(args.config))


if __name__ == '__main__':
    cli()
