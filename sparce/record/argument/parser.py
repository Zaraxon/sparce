from operator import not_, mul, eq, and_, or_, lshift

from ply import yacc

from .lexer import tokens

from ..types import Structure, Macro, Item, Time, Addrof, Become, Expr

from .errors import ParserPanicError

"""
    expr : 
        | item
        | NOT expr
        | expr MULT expr 
        | expr LSHIFT expr
        | expr AND expr
        | expr OR expr
        | expr EQUIVALENT expr
"""
def p_expr0(p):
    r'expr : NOT expr'
    p[0] = Expr((not_, p[2]))
def p_expr2(p):
    r'expr : expr MULT expr'
    p[0] = Expr((mul, p[1], p[3]))
def p_expr4(p):
    r'expr : expr LSHIFT expr'
    p[0] = Expr((lshift, p[1], p[3]))
def p_expr6(p):
    r'expr : expr AND expr'
    p[0] = Expr((and_, p[1], p[3]))
def p_expr8(p):
    r'expr : expr OR expr'
    p[0] = Expr((or_, p[1], p[3]))
def p_expr10(p):
    r'expr : expr EQUIVALENT expr'
    p[0] = Expr((eq, p[1], p[3]))
def p_expr11(p):
    r'expr : item'
    p[0] = p[1]

"""
    setcontent :
        | terminal terminal
        | terminal setcontent
"""
def p_set0(p):
    r'setcontent : terminal terminal'
    p[0] = (p[1], p[2])
def p_set1(p):
    r'setcontent : terminal setcontent'
    p[0] = (p[1], ) + p[2]

"""
    terminal:
        | STRING
        | INTEGER
        | ID
        | ADDROF ID
        | TIME
        | FLOAT 
        | ELLIPSIS
"""

def p_terminal0(p):
    r'terminal : STRING'
    p[0] = p[1]

def p_terminal1(p):
    r'terminal : INTEGER'
    p[0] = p[1]

def p_terminal2(p):
    r'terminal : ID'
    p[0] = p[1]

def p_terminal5(p):
    r'terminal : ADDROF ID'
    p[0] = Addrof(p[2])

def p_terminal7(p):
    r'terminal : TIME'
    p[0] = Time(p[1])

def p_terminal8(p):
    r'terminal : FLOAT'
    p[0] = float(p[1])

def p_terminal9(p):
    r'terminal : ELLIPSIS'
    p[0] = p[1]

"""
    become : item ARROW item
"""
def p_become(p):
    r'become : item ARROW item'
    p[0] = Become((p[1], p[3]))

"""
    list : 
        | LBRACKET content RBRACKET
        | LBRACKET RBRACKET
"""

def p_list0(p):
    r'list : LBRACKET content RBRACKET'
    p[0] = p[2]
    assert not any((isinstance(_, Item) for _ in p[2]))

def p_list1(p):
    r'list : LBRACKET RBRACKET'
    p[0] = tuple()
    assert not any((isinstance(_, Item) for _ in p[2]))


"""
    structure: LBRACE content RBRACE
"""
def p_structure(p):
    r'structure : LBRACE content RBRACE'
    stru = Structure()
    for item in p[2]:
        if isinstance(item, Item):
            name, value = item.name if item.name is not None else f'__ANOYMOUS{len(stru.keys())}__', item.value
            stru[name] = value
        else:
            name, value = f'__ANOYMOUS{len(stru.keys())}__', item
            stru[name] = value
    p[0] = stru
"""
    macro: ID LPARENTHESES content RPARENTHESES
"""
def p_macro(p):
    r'macro : ID LPARENTHESES content RPARENTHESES'
    p[0] = Macro(p[3], name=p[1])
    assert not any((isinstance(_, Item) for _ in p[3]))
"""
    content : 
        | expr
        | setcontent
        | ID EQUAL expr
        | content COMMA content
"""

def p_content2(p):
    r'content : content COMMA content'
    p[0] = p[1] + p[3]

def p_content3(p):
    r'content : expr'
    p[0] = (p[1], )

def p_content4(p):
    r'content : ID EQUAL expr'
    p[0] = (Item(name=p[1], value=p[3]), )

def p_content5(p):
    r'content : setcontent'
    p[0] = p[1]

    
"""
    item : 
        | strutcure
        | macro
        | terminal
        | list
        | become
"""

def p_item0(p):
    r'item : structure'
    p[0] = p[1]

def p_item1(p):
    r'item : macro'
    p[0] = p[1]

def p_item2(p):
    r'item : terminal'
    p[0] = p[1]

def p_item3(p):
    r'item : list'
    p[0] = p[1]

def p_item5(p):
    r'item : become'
    p[0] = p[1]

def p_error(t):
    print('general parser error, token:', t)
    print('\t next token', yacc.token())
    raise ParserPanicError()    

precedence = (
    ('left', 'COMMA', 'ARROW'), 
    ('left', 'AND'),
    ('left', 'EQUIVALENT'),
    ('left', 'OR'),
    ('left', 'LSHIFT'),
    ('left', 'MULT'),
    ('right', 'NOT'),
)


general_parser = yacc.yacc(start='content')
setattr(general_parser, '__parser_name__', 'general_parser')
