from collections import namedtuple
from typing import Any, Iterable, Iterator, Sequence, Mapping, MappingView

class Expr(tuple):
    pass

class Become(tuple):
    """
        become.from, become.to for:
        "from =>|-> to"
    """
    def __init__(self, iterable: Iterable) -> None:
        super().__init__((obj for i, obj in enumerate(iterable) if i < 2))
    
    # read-only
    @property
    def before(self):
        return self[0]
    @property
    def after(self):
        return self[1]
    
class Structure(Mapping):
    """
        单个argument, 可能表达一个结构化的参数, 也可能表达一个整数等简单参数.
    """

    def __init__(self, keys: Sequence[Any], values: Sequence[Any]):
        """
            keys: dict的keys, ordered
            values: values corresponding to keys
        """
        self.__dict = {}
        self.__key2index = {}
        self.__index2key = {}
        for index, (key, value) in enumerate(zip(keys, values)):
            if key is None:
                key = f'__ANONYMOUS{index}__'
            self.__dict[index] = value
            self.__key2index[key] = index
            self.__index2key[index] = key
        
        self.__hash = hash(tuple(((k, v) for k, v in self.__dict.items())))
        self.__keynum = len(self.__dict.keys())
    
    def __setitem__(self, key):
        raise NotImplementedError
            
    def __hash__(self) -> int:
        return self.__hash
    
    def __eq__(self, other: Any) -> bool:
        """
            __eq__ 的比较对象本身应该是一个ordered Mapping, 但不应该假设它是OrderedDict的子类.
            因此, 只检查比较对象是Mapping, 当比较对象不是ordered时是未定义行为. 
        """
        if not isinstance(other, self.__class__) and \
            not isinstance(other, Mapping):
            raise TypeError(f'cannot compare {type(other)} and {self.__class__}', other, self.__class__)

        if isinstance(other, self.__class__):
            return self.__hash == other.__hash
        else: # other is a Mapping
            same = True
            for (key, value), (okey, ovalue) in zip(self.items(), other.items()):
                if key.startswith('__ANONYMOUS') and key.endswith('__'):
                    # skip key check
                    same = same and (value == ovalue)
                else:
                    same = same and (key == okey) and (value == ovalue)
                
                if not same:
                    return same
                
            return same
    
    def __len__(self) -> int:
        if not hasattr(self, '__len'):
            self.__len = len(self.keys())
        return self.__len
    
    def keys(self):
        return tuple(self.__index2key[i] for i in range(self.__keynum))
    def values(self):
        return tuple(self[i] for i in range(self.__keynum))
    def items(self):
        return tuple((self.__index2key[i], self[i]) for i in range(self.__keynum))
    def get(self, key:str|int, default=None):
        ### 考虑到频繁使用, 还是不sanity check了

        # if not isinstance(key, str) and not isinstance(key, int):
        #     raise IndexError('invalid key', key)
        if isinstance(key, str):
            key = self.__key2index[key]
        return self.__dict.get(key, default)
    
    def __getitem__(self, key: str|int) -> Any:
        ### 考虑到频繁使用, 还是不sanity check了

        # if not isinstance(key, str) and not isinstance(key, int):
            # raise IndexError('invalid key', key)
        if isinstance(key, str):
            key = self.__key2index[key]
        return self.__dict.__getitem__(key)
    
    def __iter__(self) -> Iterator[str]:
        return iter(self.__index2key[i] for i in len(self.keys()))

    def __str__(self) -> str:
        return f'<{self.__class__} {id(self)}>'
    
    def __repr__(self) -> str:
        return '{'+''.join([f'{key}={value} ' for key, value in self.items()]).strip()+'}'

class Macro(tuple):
    
    def __new__(cls, iterable, **kwargs):
        return super(Macro, cls).__new__(cls, ( x for x in iterable))
    
    def __init__(self, iterable, name=None) -> None:
        super().__init__()
        self.name = name
    

class Item:
    """
        不对外暴露的中间态类型, 承载key=value这样的表达式用于后续构造Structure
    """

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

class Addrof(str):
    pass
