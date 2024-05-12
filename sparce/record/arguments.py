import re
from collections.abc import Iterable

class Arguments:

    ATOMS = {}
    ATOMS['HEX'] = '(\-)?0x[0-9]+'
    ATOMS['ORD'] = '(\-)?[1-9][0-9]*'
    ATOMS['OCT'] = '(\-)?0[1-9][0-9]+'
    ATOMS['INT'] = f'({ATOMS["HEX"]})' + '|' + f'({ATOMS["ORD"]})' + '|' f'({ATOMS["OCT"]})'
    ATOMS['STRING'] = '@?"(.*?)(\\\\"(.*?))*"'


    def in_nextlevel_struct(self, position: int, level: int) -> bool:
        if level+1 not in self.__structure_ranges:
            return False
        for st, ed in self.__structure_ranges[level+1]:
            if position >= st and position < ed:
                return True
        return False

    def in_string(self, position: int) -> bool:
        for st, ed in self.__string_ranges:
            if position >= st and position < ed:
                return True
        return False
        

    def process(self):
        """
            need self._line **ONLY** contain data likely to be arguments

            谨慎地处理arguments, 匹配几种可能的模式, 如果匹配失败, 则不给出任何解析
        """
        line = self._line
        self.__string_ranges = [
            (m.start(), m.end()) for m in re.finditer(self.ATOMS['STRING'], line)
        ]

        self.__structure_ranges = {}
        level, stack = 0, []
        for i, c in enumerate(line):
            
            in_str = False
            for st, ed in self.__string_ranges:
                if i >= st and i < ed:
                    in_str = True
                    break
            if in_str:
                continue

            if c in ('[', '{') and not self.in_string(i):
                level += 1
                stack.append((c, i))
            elif c in (']', '}') and not self.in_string(i):
                lc, li = stack.pop()
                if lc == '[' and c == ']':
                    if level not in self.__structure_ranges:
                        self.__structure_ranges[level] = list()
                    self.__structure_ranges[level].append((li, i+1))
                    level -= 1
                    
                elif lc == '{' and c == '}':
                    if level not in self.__structure_ranges:
                        self.__structure_ranges[level] = list()
                    self.__structure_ranges[level].append((li, i+1))
                    level -= 1
                else:
                    stack.append((lc, li))
        
        if level != 0:
            return

        self.arguments, self.argnum_all = self.parse(line, 0, 0)
        # print(self.arguments[1][1][0])
        self._line = ''
    
    def parse(self, piece: str, st_global: int, level: int) -> list | None:

        def split(piece: str, off: int) -> tuple[list[tuple[int, int]], int]:

            # 假定不会出现"call(123,,...)"这样连续的","出现
            st = 0
            args = []
            for i, c in enumerate(piece):
                if c == ',' and not self.in_nextlevel_struct(i+off, level) and not self.in_string(i+off): # 当出现有效的","
                    if st < i: # resumed 情况下可能出现 ", 123, 456", 应算作2个参数而不是3个
                        args.append((st, i))
                    st = i+1
                    while st < len(piece) and '\t\n '.find(piece[st]) >= 0:
                        st += 1
            if st < len(piece): # 在unfinished情况下可能出现"abc, def, ", 应算作2个参数而不是3个
                args.append((st, len(piece)))
            
            
            # FIXME: 处理/* 5 vars */这种注释, 放在这里递归处理不合适
            argnum_all = len(args)
            if len(args) and level == 0:
                m = re.search('/\* (?P<ARGNUM>[1-9][0-9]*) vars \*/', piece[args[-1][0]: args[-1][1]])
                if m is not None:
                    argnum_all = int(m.group('ARGNUM'))
                    args[-1] = (args[-1][0], m.start())

            return args, argnum_all
        
        if len(piece.strip()) == 0:
            return [], 0

        arguments = []
        argpieces, argnum_all = split(piece, st_global)
        for st, ed in argpieces:
        
            if piece[st] in ('{', '['):
                st += 1
            if piece[ed-1] in ('}', ']'):
                ed -= 1

            _eq = piece.find('=', st, ed)
            k, v = None, None
            if _eq >= st and _eq < ed and not self.in_string(_eq+st_global):
                k, v = piece[st: _eq], piece[_eq+1: ed]
                vst, ved = _eq+1, ed
            else:
                v = piece[st: ed]
                vst, ved = st, ed
            

            if self.in_nextlevel_struct(vst+st_global, level) and self.in_nextlevel_struct(ved-1+st_global, level):
                vlist, _ = self.parse(v, vst+st_global, level+1)
                v = vlist

            arguments.append((k, v))

        return arguments, argnum_all

    def to_string(self) -> str:
        
        if self.arguments is None:
            return ''

        return f'{len(self.arguments)}/{self.argnum_all} arguments'

    def to_serialized(
            self,
            value_only=True
            ) -> str:
        
        if not self.arguments:
            return ''
        else:
            return self._to_serialized(self.arguments, value_only)
    
    def _to_serialized(
            self,
            arguments, 
            value_only=True
            ) -> str:
        
        if not arguments:
            return ''
        
        to_string = ''
        for k, v in arguments:

            if not isinstance(v, list):
                _to_string = str(v)
            else:
                _to_string = Arguments._to_serialized(self, v, value_only)
            
            if not value_only:
                _to_string = str(k) + '=' + _to_string
            
            to_string += _to_string + ','

        to_string = to_string.rstrip(',')

        return f'[{to_string}]'
        