from .lexer import tokens

from ..types import Structure, Macro, Item, Time, _Ellipsis

from ply import yacc

"""
nameditem:
    | ID EQUAL item

item:
    | structure
    | macro
    | expression
    | list

content_sequence:
    | item
    | named_item
    | content_sequence COMMA content_sequence

list:
    | LBRACKET content_sequence RBRACKET
structure:
    | LBRACE content_sequence RBRACE
macro:
    | ID LPARENTHESES content_sequence RPARENTHESES

expression:
    | STRING
    | literal_expression
    | INTEGER ARROW INTEGER
    | TIME
    | ELLIPSIS
    | FLOAT

literal_expression:
    | ID
    | INTEGER
    | literal_expression OR literal_expression

"""

def p_literal_expression_id(p):
    r'literal_expression : ID'
    p[0] = p[1]

def p_literal_expression_integer(p):
    r'literal_expression : INTEGER'
    p[0] = p[1]

def p_literal_expression_or(p):
    r'literal_expression : literal_expression OR literal_expression'
    p[0] = str(p[1])+str(p[2])+str(p[3])

def p_expression_string(p):
    r'expression : STRING'
    p[0] = p[1]

def p_expression_literal_expression(p):
    r'expression : literal_expression'
    p[0] = p[1]

def p_expression_integer2integer(p):
    r'expression : INTEGER ARROW INTEGER'
    p[0] = p[3]

def p_expression_time(p):
    r'expression : TIME'
    p[0] = Time(p[1])

def p_expression_float(p):
    r'expression : FLOAT'
    p[0] = float(p[1])

def p_expression_ellipsis(p):
    r'expression : ELLIPSIS'
    p[0] = _Ellipsis(p[1])

def p_list(p):
    r'list : LBRACKET content_sequence RBRACKET'
    p[0] = p[2]

def p_structure(p):
    r'structure : LBRACE content_sequence RBRACE'
    stru = Structure()
    for item in p[2]:
        name, value = item.name if item.name is not None else f'__ANOYMOUS{len(stru.keys())}__', item.value
        stru[name] = value
    p[0] = stru

def p_macro(p):
    r'macro : ID LPARENTHESES content_sequence RPARENTHESES'
    macro = Macro()
    for item in p[3]:
        name, value = item.name if item.name is not None else f'__ANOYMOUS{len(macro.keys())}__', item.value
        macro[name] = value
    macro.name = p[1]
    p[0] = macro

def p_content_sequence_item(p):
    r'content_sequence : item'
    p[0] = (p[1], )

def p_content_sequence_named_item(p):
    r'content_sequence : named_item'
    p[0] = (p[1], )

def p_content_sequence_sequence(p):
    r'content_sequence : content_sequence COMMA content_sequence'
    p[0] = p[1] + p[3]

def p_item_structure(p):
    r'item : structure'
    p[0] = Item(None, p[1])

def p_item_macro(p):
    r'item : macro'
    p[0] = Item(None, p[1])

def p_item_expression(p):
    r'item : expression'
    p[0] = Item(None, p[1])

def p_item_list(p):
    r'item : list'
    p[0] = Item(None, p[1])
    
def p_named_item(p):
    r'named_item : ID EQUAL item'
    p[0] = Item(p[1], p[3].value)

precedence = (
    ('left', 'COMMA'),
    ('left', 'OR')
)


parser = yacc.yacc(start='content_sequence')

