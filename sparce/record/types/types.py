from collections import OrderedDict
from typing import Any

class Structure(OrderedDict):
    """
        单个argument, 可能表达一个结构化的参数, 也可能表达一个整数等简单参数.
    """
    
    def __getitem__(self, key: Any) -> Any:
        if isinstance(key, int):
            try:
                return self[self.keys()[key]]
            except IndexError:
                raise IndexError(f'trying indexing {key} out of {len(self.keys())} members')
        elif isinstance(key, str):
            try:
                return super().__getitem__(key)
            except KeyError:
                raise KeyError(f'{self.keys()} not in members :[{key}]')
        else:
            raise TypeError(f'key must be int or str, but got {type(key)}: {key}')
    
    def __str__(self) -> str:
        return '{'+''.join([f'{key}={value} ' for key, value in self.items()]).strip()+'}'
    
    def __repr__(self) -> str:
        return str(self)

class Macro(Structure):
    
    def __init__(self, *args, **kwargs) -> None:
        self.name = kwargs.pop('name', None)
        super().__init__(*args, **kwargs)

class Item:

    def __init__(self, name, value) -> None:
        self._name = name
        self._value = value
    
    def __str__(self) -> str:
        return f'{str(self.name)}={str(self.value)}' if self.name else str(self.value)
    
    def __repr__(self) -> str:
        return str(self)
    
    # read-only properties
    @property
    def name(self) -> str:
        return self._name
    @property
    def value(self) -> Any:
        return self._value

class Time(str):
    pass

class _Ellipsis(str):
    pass
