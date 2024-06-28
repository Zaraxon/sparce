from typing import Any
from ast import literal_eval
from enum import IntFlag, Enum
# aenum==3.1.1
from aenum import extend_enum
from string import digits

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

    def to_oct (data) -> int|None:
        is_oct = True
        if len(data) < 2 or data[0] != '0':
            return
        for _ in data[1:]:
            if _ not in digits:
                is_oct = False
                break
        # 修复Python的八进制格式, try again
        if is_oct: 
            data = data[0]+'o'+data[1:]
            return data
        
    name, data = data[0], data[1]
    
    if not isinstance(data, str):
        return tuple([name, tuple([_ArgumentConstructor(d) for d in data])])
    
    try:
        # 如果是字面值, 直接求值
        _ifoct = to_oct(data) # 首先排除单个八进制
        if _ifoct:
            return name, literal_eval(_ifoct)
        return name, literal_eval(data)
    except (ValueError, SyntaxError):
        # 如果不是字面值, 则只可能是某些标志码和数字的或
        if '|' in data:
            code = SysFlag.NONE
            for c in data.strip().split('|'):
                try:
                    c = literal_eval(c)
                except (ValueError, SyntaxError):
                    _ifoct = to_oct(c) # 首先排除单个八进制
                    if _ifoct:
                        c = literal_eval(_ifoct)
                    else:
                        if c not in SysFlag._member_names_:
                            extend_enum(SysFlag, c, 1<<len(SysFlag.__members__))
                        c = getattr(SysFlag, c)
                code |= c

            return name, code
        else:
            _ifoct = to_oct(data) # 首先排除单个八进制
            if _ifoct:
                code = literal_eval(_ifoct)
            else:
                if data not in SysFlag._member_names_:
                    extend_enum(SysFlag, data, 1<<len(SysFlag.__members__))
                code = getattr(SysFlag, data)
            return name, code

        
def RetvalConstructor(data):
    if data.strip() == '?':
        return None
    retval = literal_eval(data)
    assert isinstance(retval, int)
    return retval

PROPERTIES_GENERAL = {
    'pid': int,
    'timestamp': float,
    'arguments': ArgumentConstructor,
    'retval': RetvalConstructor
}