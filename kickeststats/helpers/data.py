from itertools import zip_longest
from typing import Iterable, Any


def grouper(iterable: Iterable, n: int, fillvalue: Any = None) -> Iterable:
    """
    Collect data into fixed-length chunks or blocks
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
