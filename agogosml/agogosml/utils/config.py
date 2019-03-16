"""Configuration utilities."""
from ast import literal_eval
from json import JSONDecodeError
from json import loads


class Config:
    """Dictionary wrapper that converts string values to Python objects."""

    def __init__(self, config):
        """Wrap the given configuration dictionary."""
        self.__config = config

    def __getitem__(self, item):
        """Get a key."""
        value = self.__config[item]
        return to_python(value)

    def get(self, item, default=None):
        """Get a key or the default value if the key doesn't exist."""
        try:
            return self[item]
        except KeyError:
            return default


def to_python(value):
    """
    Convert a string value to a python object.

    >>> json_value = '{"foo": "bar"}'
    >>> to_python(json_value)
    {'foo': 'bar'}
    >>> ast_value = "[1, '2', 3]"
    >>> to_python(ast_value)
    [1, '2', 3]
    >>> string_value = 'value'
    >>> to_python(string_value)
    'value'
    >>> already_parsed_value = ['a', 1]
    >>> to_python(already_parsed_value)
    ['a', 1]
    """
    if not isinstance(value, str):
        return value

    try:
        return loads(value)
    except JSONDecodeError:
        pass

    try:
        return literal_eval(value)
    except (SyntaxError, ValueError):
        pass

    return value
