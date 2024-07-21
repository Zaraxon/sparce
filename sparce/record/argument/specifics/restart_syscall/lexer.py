from ply.lex import lex

from ...errors import LexerPanicError

tokens = ('ANY', )

def t_ANY(t):
    r'.+'

def t_error(t):
    raise LexerPanicError()

restart_syscall_lexer = lex()