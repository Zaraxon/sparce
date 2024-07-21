from ply.yacc import yacc

from ...errors import ParserPanicError

from .lexer import tokens

def p_all0(p):
    r'all : ANY'
    p[0] = tuple()

def p_all1(p):
    r'all : '
    p[0] = tuple()

def p_error(t):
    raise ParserPanicError()

restart_syscall_parser = yacc(start='all')