from ply import lex
from ast import literal_eval
from ..types import Time, _Ellipsis


tokens = ('STRING', 'ID', 'INTEGER', 'EQUAL', 'COMMA', 'LPARENTHESES', 
          'RPARENTHESES', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 
          'OR', 'ARROW', 'TIME', 'ELLIPSIS', 'FLOAT')

def t_STRING(t): 
    r'@?"(.*?)(\\"(.*?))*?"'
    if t.value[0] == '@':
        t.value = t.value[1:]
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
    t.value = _Ellipsis(t.value)
    return t


def t_ignore_COMMENT(t):
    r'/\*.*?\*/'

def t_ignore_BLANK(t):
    r'\s+'


t_ARROW = r'(=>)|(->)'
t_EQUAL = r'='
t_COMMA = r','
t_LPARENTHESES = r'\('
t_RPARENTHESES = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_OR = r'\|'

lexer = lex.lex()