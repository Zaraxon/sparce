from ply import lex, yacc
from ....types import Structure
from ...errors import ParserPanicError

from .lexer import tokens, ioctl_lexer

"""
    ioctlTCGETSargs : fd COMMA TCGETStag COMMA TCGETStermios 
    fd: INTEGER
    TCGETStermios : LBRACE TCGETSargstring RBRACE
    TCGETSargstring : 
        | TCGETSarg
        | ELLIPSIS
        | TCGETSarg TCGETSargstring
"""

def p_ioctlTCGETSargs(p):
    r"ioctlTCGETSargs : fd COMMA TCGETStag COMMA TCGETStermios"
    p[0] = (p[1], p[3], p[5]) 

def p_fd(p):
    r'fd : INTEGER'
    p[0] = p[1]

def p_TCGETStermios(p):
    r'TCGETStermios : LBRACE TCGETSargstring RBRACE'
    # 注意与通用解析器那边一致
    stru = Structure()
    for TCGETSarg in p[2]:
        stru[f'__ANONYMOUS{len(stru.keys())}__'] = TCGETSarg
    p[0] = stru

def p_TCGETSargstring0(p):
    r'TCGETSargstring : TCGETSarg'
    p[0] = (p[1], )

def p_TCGETSargstring1(p):
    r'TCGETSargstring : ELLIPSIS'
    p[0] = (Ellipsis, )

def p_TCGETSargstring2(p):
    r'TCGETSargstring : TCGETSarg TCGETSargstring'
    p[0] = (p[1], ) + p[2]

def p_error(p):
    raise ParserPanicError()

ioctl_parser = yacc.yacc(start='ioctlTCGETSargs')
setattr(ioctl_parser, '__parser_name__', 'ioctl_parser')