from ast import literal_eval

from enum import IntFlag
from aenum import extend_enum

from functools import reduce
from operator import or_


from ....record.prop import PropertyConstructionError

class BufferPropertyError(PropertyConstructionError):
    pass

def buffer(bufstr: str) -> bytes:
    
    if not isinstance(bufstr, str):
        raise BufferPropertyError(f'constructing buffer failed, errdata:{bufstr}')
    
    if bufstr.startswith('"') and bufstr.endswith('"'):
        return literal_eval(bufstr.encode('raw-unicode-escape').decode('raw-unicode-escape')).encode('utf-8')
    else:
        raise BufferPropertyError(f'constructing buffer failed, errdata:{bufstr}')

def IntorIntFlag(s: str, flag: IntFlag) -> int|IntFlag:
    
    def single(s: str) -> int:
        try:
            return int(s, 0)
        except ValueError:
            return flag[s]
        
    return reduce(
        or_,
        [single(_) for _ in s.split('|')],
        0
    )
