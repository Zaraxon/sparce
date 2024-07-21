
from ply.lex import lex
from ply.yacc import yacc

from .argument import \
    general_parser, general_lexer, \
    ioctl_lexer, ioctl_parser, \
    restart_syscall_lexer, restart_syscall_parser

from .argument.errors import LexerPanicError, ParserPanicError

from .errors import ArgumentsParsingError

class Arguments:
    
    def process(self):
        """
            need self._line **ONLY** contain data likely to be arguments

            谨慎地处理arguments, 匹配几种可能的模式, 如果匹配失败, 则不给出任何解析
        """
        
        self._line = self._line.strip()
        if self._line == '':
            return
        if self._line[-1] == ',':
            self._line = self._line[:-1]
        elif self._line[0] == ',':
            self._line = self._line[1:]
        
        parsers = {
            'ioctl': (ioctl_parser, ioctl_lexer),
            'restart_syscall': (restart_syscall_parser, restart_syscall_lexer)
        }
        
        line = self._line
        
        # try general lexer first
        try:
            self.arguments = general_parser.parse(line, lexer=general_lexer)
        except (LexerPanicError, ParserPanicError):
            self.arguments = None

        if hasattr(self, 'syscall') and self.arguments is None:
            for syscall_name, (parser, lexer) in parsers.items():
                if self.syscall == syscall_name:
                    try:
                        self.arguments = parser.parse(line, lexer=lexer)
                        break
                    except (LexerPanicError, ParserPanicError):
                        self.arguments = None
        
        if self.arguments is None:
            raise ArgumentsParsingError(self._line)
        
        self._line = ''
    
    def to_string(self) -> str:
        
        if self.arguments is None:
            return ''
        return str(self.arguments)

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
        