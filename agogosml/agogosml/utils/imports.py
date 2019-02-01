"""Utilities for imports"""
from importlib import import_module
from inspect import getsourcefile
from pathlib import Path
from pkgutil import walk_packages
from typing import Iterable
from typing import Tuple
from typing import Type
from typing import TypeVar

SomeClass = TypeVar('SomeClass')
Interface = Type[SomeClass]


def get_base_module(interface: Interface) -> Tuple[str, Path]:
    """Get the base module of an interface."""
    base_module_name = '.'.join(interface.__module__.split('.')[:-1])
    base_module_path = Path(getsourcefile(interface)).parent
    return base_module_name, base_module_path


def import_subpackages(module_prefix: str, module_path: Path):
    """Import all subpackages of a module."""
    for _, module, _ in walk_packages([str(module_path)]):
        sub_module_name = '%s.%s' % (module_prefix, module)
        import_module(sub_module_name)


def find_implementations(interface: Interface) -> Iterable[Interface]:
    """Find implementations of the interface."""
    base_module_name, base_module_path = get_base_module(interface)
    import_subpackages(base_module_name, base_module_path)
    return interface.__subclasses__()
