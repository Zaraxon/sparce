from ply.lex import LexError

from .argument import parser

class Arguments:
    
    def process(self):
        """
            need self._line **ONLY** contain data likely to be arguments

            谨慎地处理arguments, 匹配几种可能的模式, 如果匹配失败, 则不给出任何解析
        """
        self.arguments = parser.parse(self._line)
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
        