from importlib import import_module
from inspect import getsourcefile
from pathlib import Path
from pkgutil import walk_packages
from typing import Iterable
from typing import Tuple
from typing import Type
from typing import TypeVar

T = TypeVar('T')


def get_base_module(interface) -> Tuple[str, Path]:
    base_module_name = '.'.join(interface.__module__.split('.')[:-1])
    base_module_path = Path(getsourcefile(interface)).parent
    return base_module_name, base_module_path


def import_subpackages(module_prefix: str, module_path: Path):
    for _, module, _ in walk_packages([str(module_path)]):
        sub_module_name = '%s.%s' % (module_prefix, module)
        import_module(sub_module_name)


def find_implementations(interface: Type[T]) -> Iterable[Type[T]]:
    base_module_name, base_module_path = get_base_module(interface)
    import_subpackages(base_module_name, base_module_path)
    return interface.__subclasses__()
