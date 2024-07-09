
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'content_sequenceleftCOMMAleftORARROW COMMA ELLIPSIS EQUAL FLOAT ID INTEGER LBRACE LBRACKET LPARENTHESES OR RBRACE RBRACKET RPARENTHESES STRING TIMEliteral_expression : IDliteral_expression : INTEGERliteral_expression : literal_expression OR literal_expressionexpression : STRINGexpression : literal_expressionexpression : INTEGER ARROW INTEGERexpression : TIMEexpression : FLOATexpression : ELLIPSISlist : LBRACKET content_sequence RBRACKETstructure : LBRACE content_sequence RBRACEmacro : ID LPARENTHESES content_sequence RPARENTHESEScontent_sequence : itemcontent_sequence : named_itemcontent_sequence : content_sequence COMMA content_sequenceitem : structureitem : macroitem : expressionitem : listnamed_item : ID EQUAL item'
    
_lr_action_items = {'ID':([0,9,16,17,18,19,21,],[8,8,8,8,25,8,30,]),'LBRACE':([0,9,16,17,18,19,],[9,9,9,9,9,9,]),'STRING':([0,9,16,17,18,19,],[10,10,10,10,10,10,]),'INTEGER':([0,9,16,17,18,19,21,22,],[12,12,12,12,12,12,31,32,]),'TIME':([0,9,16,17,18,19,],[13,13,13,13,13,13,]),'FLOAT':([0,9,16,17,18,19,],[14,14,14,14,14,14,]),'ELLIPSIS':([0,9,16,17,18,19,],[15,15,15,15,15,15,]),'LBRACKET':([0,9,16,17,18,19,],[16,16,16,16,16,16,]),'$end':([1,2,3,4,5,6,7,8,10,11,12,13,14,15,24,25,26,28,29,30,31,32,33,34,],[0,-13,-14,-16,-17,-18,-19,-1,-4,-5,-2,-7,-8,-9,-15,-1,-20,-11,-3,-1,-2,-6,-10,-12,]),'COMMA':([1,2,3,4,5,6,7,8,10,11,12,13,14,15,20,23,24,25,26,27,28,29,30,31,32,33,34,],[17,-13,-14,-16,-17,-18,-19,-1,-4,-5,-2,-7,-8,-9,17,17,-15,-1,-20,17,-11,-3,-1,-2,-6,-10,-12,]),'RBRACE':([2,3,4,5,6,7,8,10,11,12,13,14,15,20,24,25,26,28,29,30,31,32,33,34,],[-13,-14,-16,-17,-18,-19,-1,-4,-5,-2,-7,-8,-9,28,-15,-1,-20,-11,-3,-1,-2,-6,-10,-12,]),'RBRACKET':([2,3,4,5,6,7,8,10,11,12,13,14,15,23,24,25,26,28,29,30,31,32,33,34,],[-13,-14,-16,-17,-18,-19,-1,-4,-5,-2,-7,-8,-9,33,-15,-1,-20,-11,-3,-1,-2,-6,-10,-12,]),'RPARENTHESES':([2,3,4,5,6,7,8,10,11,12,13,14,15,24,25,26,27,28,29,30,31,32,33,34,],[-13,-14,-16,-17,-18,-19,-1,-4,-5,-2,-7,-8,-9,-15,-1,-20,34,-11,-3,-1,-2,-6,-10,-12,]),'EQUAL':([8,],[18,]),'LPARENTHESES':([8,25,],[19,19,]),'OR':([8,11,12,25,29,30,31,],[-1,21,-2,-1,-3,-1,-2,]),'ARROW':([12,],[22,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'content_sequence':([0,9,16,17,19,],[1,20,23,24,27,]),'item':([0,9,16,17,18,19,],[2,2,2,2,26,2,]),'named_item':([0,9,16,17,19,],[3,3,3,3,3,]),'structure':([0,9,16,17,18,19,],[4,4,4,4,4,4,]),'macro':([0,9,16,17,18,19,],[5,5,5,5,5,5,]),'expression':([0,9,16,17,18,19,],[6,6,6,6,6,6,]),'list':([0,9,16,17,18,19,],[7,7,7,7,7,7,]),'literal_expression':([0,9,16,17,18,19,21,],[11,11,11,11,11,11,29,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> content_sequence","S'",1,None,None,None),
  ('literal_expression -> ID','literal_expression',1,'p_literal_expression_id','parser.py',45),
  ('literal_expression -> INTEGER','literal_expression',1,'p_literal_expression_integer','parser.py',49),
  ('literal_expression -> literal_expression OR literal_expression','literal_expression',3,'p_literal_expression_or','parser.py',53),
  ('expression -> STRING','expression',1,'p_expression_string','parser.py',57),
  ('expression -> literal_expression','expression',1,'p_expression_literal_expression','parser.py',61),
  ('expression -> INTEGER ARROW INTEGER','expression',3,'p_expression_integer2integer','parser.py',65),
  ('expression -> TIME','expression',1,'p_expression_time','parser.py',69),
  ('expression -> FLOAT','expression',1,'p_expression_float','parser.py',73),
  ('expression -> ELLIPSIS','expression',1,'p_expression_ellipsis','parser.py',77),
  ('list -> LBRACKET content_sequence RBRACKET','list',3,'p_list','parser.py',81),
  ('structure -> LBRACE content_sequence RBRACE','structure',3,'p_structure','parser.py',85),
  ('macro -> ID LPARENTHESES content_sequence RPARENTHESES','macro',4,'p_macro','parser.py',93),
  ('content_sequence -> item','content_sequence',1,'p_content_sequence_item','parser.py',102),
  ('content_sequence -> named_item','content_sequence',1,'p_content_sequence_named_item','parser.py',106),
  ('content_sequence -> content_sequence COMMA content_sequence','content_sequence',3,'p_content_sequence_sequence','parser.py',110),
  ('item -> structure','item',1,'p_item_structure','parser.py',114),
  ('item -> macro','item',1,'p_item_macro','parser.py',118),
  ('item -> expression','item',1,'p_item_expression','parser.py',122),
  ('item -> list','item',1,'p_item_list','parser.py',126),
  ('named_item -> ID EQUAL item','named_item',3,'p_named_item','parser.py',130),
]