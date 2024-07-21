from ply import lex
from ast import literal_eval

from ..types import Time
from .errors import LexerPanicError

tokens = ('STRING', 'ID', 'INTEGER', 'EQUAL', 'COMMA', 'LPARENTHESES', 
          'RPARENTHESES', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 
          'OR', 'ARROW', 'TIME', 'ELLIPSIS', 'FLOAT', 'MULT', 'ADDROF', 'NOT', 'LSHIFT', 'AND', 'EQUIVALENT')

def t_STRING(t): 
    r'@?"(.*?)(\\".*?)*?"(\.\.\.)?'
    if t.value[0] == '@':
        t.value = t.value[1:]
    if t.value[-3:] == r'...':
        t.value = t.value[:-3]
    t.value = literal_eval(t.value.encode('raw-unicode-escape').decode('raw-unicode-escape')).encode('utf-8')
    return t

def t_ID(t): 
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_TIME(t):
    r'\d+/\d+/\d+-\d+:\d+:\d+(\.[0-9]+)?'
    t.value = Time(t.value)
    return t

def t_FLOAT(t):
    r'-?[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'(-?[1-9][0-9]*)|(0x[0-9a-f]+)|(0[0-7]+)|0+'
    if t.value[0] == '0' and t.value[:2] != '0x' and len(t.value) > 1: # 八进制
        t.value = '0o'+t.value[1:]
    t.value = int(t.value, 0)
    return t

def t_ELLIPSIS(t):
    r'\.\.\.'
    t.value = Ellipsis
    return t

def t_ignore_COMMENT(t):
    r'/\*.*?\*/'

def t_ignore_BLANK(t):
    r'\s+'

def t_error(t):
    raise LexerPanicError()

t_LSHIFT = r'<<'
t_ARROW = r'(=>)|(->)'
t_EQUIVALENT = r'=='
t_EQUAL = r'='
t_COMMA = r','
t_LPARENTHESES = r'\('
t_RPARENTHESES = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_MULT = r'\*'
t_AND = r'&&'
t_ADDROF = r'&'
t_OR = r'\|'
t_NOT = r'~'

general_lexer = lex.lex()
setattr(general_lexer, '__lexer_name__', 'general_lexer')