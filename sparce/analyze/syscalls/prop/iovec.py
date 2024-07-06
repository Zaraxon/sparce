from typing import Iterable

from ....record.prop import PropertyConstructionError

from ..struct.iovec import iovec as iovec_stru

from .common import buffer

def iovec(arguments: list, iov_base_constructors: Iterable=None) -> iovec_stru:

    if iov_base_constructors is None:
        iov_base_constructors = [buffer]

    iov_base, iov_len = None, int(arguments[1][1], 0)
    for iov_base_constructor in iov_base_constructors:
        try:
            iov_base = iov_base_constructor(arguments[0][1])
            return iovec_stru((iov_base, iov_len))
        except PropertyConstructionError:
            pass
    
    raise PropertyConstructionError(f"Could not construct iov_base from {arguments[0][1]}, constructors: {[_.__name__ for _ in iov_base_constructors]}")
    