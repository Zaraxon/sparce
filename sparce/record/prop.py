from typing import Any
from ast import literal_eval
from enum import IntFlag, Enum
# aenum==3.1.1
from aenum import extend_enum

class _ToProperty(type):
    pass

def __process(self):
    for name, constructor in self.__props__.items():
        if not hasattr(self, name) or getattr(self, name) is None:
            _str = f'not hasattr {name}' if not hasattr(self, name) else f'{name} is None'
            raise RuntimeError(_str)
        setattr(self, name, constructor(getattr(self, name)))

def Property(props: dict):
    """
        将一组**预期存在**的属性从字符串解析为Python原语
        例如 syscall_record.pid == '58' -> syscall_record.pid == 58 (int类型)
        
        props: {属性名: 构造器}
        构造器用来从一个单个的字符串解析为Python原语(int, str等) 
        简单结构可以直接传参Python类, 嵌套结构协议需要自定义实现
        e.g.
            Property(
                {'abc': int},
                {'xyz': str},
                {'cbd': tuple}
            )
    """
    return type.__new__(_ToProperty, 'ToProperty', (), {'__props__': props, 'process': __process})

"""
    constructors
"""

class SysFlag(IntFlag):
    __str__ = Enum.__str__

    NONE = 0

def ArgumentConstructor(data):
    return tuple([_ArgumentConstructor(d) for d in data])

def _ArgumentConstructor(data):

    name, data = data[0], data[1]
    
    if not isinstance(data, str):
        return name, tuple([_ArgumentConstructor(d) for d in data])
    
    try:
        # 如果是字面值, 直接求值
        return name, literal_eval(data)
    except ValueError:
        # 如果不是字面值, 则只可能是某些标志码的或
        
        code = SysFlag.NONE
        for c in data.strip().split('|'):
            try:
                c = literal_eval(c)
            except ValueError:
                if c not in SysFlag._member_names_:
                    extend_enum(SysFlag, c, 1<<len(SysFlag.__members__))
                c = getattr(SysFlag, c)
            code |= c

        return name, code
