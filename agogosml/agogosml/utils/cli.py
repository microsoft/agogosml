"""Utilities for CLIs."""
from argparse import ArgumentTypeError
from json import loads


def json_arg(value: str):
    """
    Parse a JSON argument from the command line.

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
