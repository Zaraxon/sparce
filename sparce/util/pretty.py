from ..record.record import Record
from ..record.prop import SysFlag
from operator import add
from functools import reduce


def pretty_arguments(record: Record) -> str:
    
    def _pretty_arguments_recursive(data) -> str:
        if (isinstance(data, tuple) or isinstance(data, list)) and len(data) == 2:
            name, data = data[0], data[1]
        else:
            return str(data)
        if isinstance(data, list) or isinstance(data, tuple):
            return '['+reduce(add, [_pretty_arguments_recursive(_)+',' for _ in data], '').rstrip(',')+']'
        if name is not None:
            return f'<{name}={str(data)}>' if not isinstance(data, SysFlag) else f'<{name}={data.name}>'
        else :
            return f'<{str(data)}>' if not isinstance(data, SysFlag) else f'<{data.name}>'
        
    if not hasattr(record, 'arguments') or record.arguments is None:
        return ''
    
    return 'arguments'+'['+reduce(add, [_pretty_arguments_recursive(_)+',' for _ in record.arguments], '').rstrip(',')+']'
    