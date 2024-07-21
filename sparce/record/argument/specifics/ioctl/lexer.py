from ply import lex

from ...errors import LexerPanicError

tokens = ('ELLIPSIS', 'TCGETSarg', 'COMMA', 'LBRACE', 'RBRACE', 'INTEGER', 'TCGETStag')

def t_INTEGER(t):
    r'(-?[1-9][0-9]*)|(0x[0-9a-f]+)|(0[0-7]+)|0+'
    if t.value[0] == '0' and t.value[:2] != '0x' and len(t.value) > 1: # 八进制
        t.value = '0o'+t.value[1:]
    t.value = int(t.value, 0)
    return t

def t_TCGETStag(t):
    r'TCGETS'
    return t

def t_TCGETSarg(t):
    r'-?[a-zA-Z_][a-zA-Z0-9_]*'
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

t_COMMA = r','
t_LBRACE = r'\{'
t_RBRACE = r'\}'

ioctl_lexer = lex.lex()
setattr(ioctl_lexer, '__lexer_name__', 'ioctl_lexer')