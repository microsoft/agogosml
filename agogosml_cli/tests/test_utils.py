"""Test utility functions"""


import hashlib
from pathlib import Path
from typing import Union


def md5(path: Union[Path, str]):
    """Compute the md5 of a file"""
    path = Path(path)
    hash_md5 = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
