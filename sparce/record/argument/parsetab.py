
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'contentleftCOMMAARROWleftANDleftEQUIVALENTleftORleftLSHIFTleftMULTrightNOTADDROF AND ARROW COMMA ELLIPSIS EQUAL EQUIVALENT FLOAT ID INTEGER LBRACE LBRACKET LPARENTHESES LSHIFT MULT NOT OR RBRACE RBRACKET RPARENTHESES STRING TIMEexpr : NOT exprexpr : expr MULT exprexpr : expr LSHIFT exprexpr : expr AND exprexpr : expr OR exprexpr : expr EQUIVALENT exprexpr : itemsetcontent : terminal terminalsetcontent : terminal setcontentterminal : STRINGterminal : INTEGERterminal : IDterminal : ADDROF IDterminal : TIMEterminal : FLOATterminal : ELLIPSISbecome : item ARROW itemlist : LBRACKET content RBRACKETlist : LBRACKET RBRACKETstructure : LBRACE content RBRACEmacro : ID LPARENTHESES content RPARENTHESEScontent : content COMMA contentcontent : exprcontent : ID EQUAL exprcontent : setcontentitem : structureitem : macroitem : terminalitem : listitem : become'
    
_lr_action_items = {'ID':([0,3,5,7,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,31,32,34,35,],[3,-12,30,34,-10,-11,35,-14,-15,-16,3,3,3,30,30,30,30,30,30,3,30,34,-12,-13,]),'NOT':([0,5,18,19,20,21,22,23,24,25,26,27,],[5,5,5,5,5,5,5,5,5,5,5,5,]),'STRING':([0,3,5,7,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,31,32,34,35,],[12,-12,12,12,-10,-11,-14,-15,-16,12,12,12,12,12,12,12,12,12,12,12,12,-12,-13,]),'INTEGER':([0,3,5,7,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,31,32,34,35,],[13,-12,13,13,-10,-11,-14,-15,-16,13,13,13,13,13,13,13,13,13,13,13,13,-12,-13,]),'ADDROF':([0,3,5,7,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,31,32,34,35,],[14,-12,14,14,-10,-11,-14,-15,-16,14,14,14,14,14,14,14,14,14,14,14,14,-12,-13,]),'TIME':([0,3,5,7,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,31,32,34,35,],[15,-12,15,15,-10,-11,-14,-15,-16,15,15,15,15,15,15,15,15,15,15,15,15,-12,-13,]),'FLOAT':([0,3,5,7,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,31,32,34,35,],[16,-12,16,16,-10,-11,-14,-15,-16,16,16,16,16,16,16,16,16,16,16,16,16,-12,-13,]),'ELLIPSIS':([0,3,5,7,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,31,32,34,35,],[17,-12,17,17,-10,-11,-14,-15,-16,17,17,17,17,17,17,17,17,17,17,17,17,-12,-13,]),'LBRACE':([0,5,18,19,20,21,22,23,24,25,26,27,31,],[18,18,18,18,18,18,18,18,18,18,18,18,18,]),'LBRACKET':([0,5,18,19,20,21,22,23,24,25,26,27,31,],[19,19,19,19,19,19,19,19,19,19,19,19,19,]),'$end':([1,2,3,4,6,7,8,9,10,11,12,13,15,16,17,28,29,30,32,33,34,35,38,39,40,41,42,43,44,45,47,48,49,50,],[0,-23,-12,-25,-7,-28,-26,-27,-29,-30,-10,-11,-14,-15,-16,-1,-28,-12,-8,-9,-12,-13,-19,-22,-2,-3,-4,-5,-6,-24,-17,-20,-18,-21,]),'COMMA':([1,2,3,4,6,7,8,9,10,11,12,13,15,16,17,28,29,30,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,],[20,-23,-12,-25,-7,-28,-26,-27,-29,-30,-10,-11,-14,-15,-16,-1,-28,-12,-8,-9,-12,-13,20,20,-19,-22,-2,-3,-4,-5,-6,-24,20,-17,-20,-18,-21,]),'RBRACE':([2,3,4,6,7,8,9,10,11,12,13,15,16,17,28,29,30,32,33,34,35,36,38,39,40,41,42,43,44,45,47,48,49,50,],[-23,-12,-25,-7,-28,-26,-27,-29,-30,-10,-11,-14,-15,-16,-1,-28,-12,-8,-9,-12,-13,48,-19,-22,-2,-3,-4,-5,-6,-24,-17,-20,-18,-21,]),'RBRACKET':([2,3,4,6,7,8,9,10,11,12,13,15,16,17,19,28,29,30,32,33,34,35,37,38,39,40,41,42,43,44,45,47,48,49,50,],[-23,-12,-25,-7,-28,-26,-27,-29,-30,-10,-11,-14,-15,-16,38,-1,-28,-12,-8,-9,-12,-13,49,-19,-22,-2,-3,-4,-5,-6,-24,-17,-20,-18,-21,]),'RPARENTHESES':([2,3,4,6,7,8,9,10,11,12,13,15,16,17,28,29,30,32,33,34,35,38,39,40,41,42,43,44,45,46,47,48,49,50,],[-23,-12,-25,-7,-28,-26,-27,-29,-30,-10,-11,-14,-15,-16,-1,-28,-12,-8,-9,-12,-13,-19,-22,-2,-3,-4,-5,-6,-24,50,-17,-20,-18,-21,]),'MULT':([2,3,6,7,8,9,10,11,12,13,15,16,17,28,29,30,35,38,40,41,42,43,44,45,47,48,49,50,],[21,-12,-7,-28,-26,-27,-29,-30,-10,-11,-14,-15,-16,-1,-28,-12,-13,-19,-2,21,21,21,21,21,-17,-20,-18,-21,]),'LSHIFT':([2,3,6,7,8,9,10,11,12,13,15,16,17,28,29,30,35,38,40,41,42,43,44,45,47,48,49,50,],[22,-12,-7,-28,-26,-27,-29,-30,-10,-11,-14,-15,-16,-1,-28,-12,-13,-19,-2,-3,22,22,22,22,-17,-20,-18,-21,]),'AND':([2,3,6,7,8,9,10,11,12,13,15,16,17,28,29,30,35,38,40,41,42,43,44,45,47,48,49,50,],[23,-12,-7,-28,-26,-27,-29,-30,-10,-11,-14,-15,-16,-1,-28,-12,-13,-19,-2,-3,-4,-5,-6,23,-17,-20,-18,-21,]),'OR':([2,3,6,7,8,9,10,11,12,13,15,16,17,28,29,30,35,38,40,41,42,43,44,45,47,48,49,50,],[24,-12,-7,-28,-26,-27,-29,-30,-10,-11,-14,-15,-16,-1,-28,-12,-13,-19,-2,-3,24,-5,24,24,-17,-20,-18,-21,]),'EQUIVALENT':([2,3,6,7,8,9,10,11,12,13,15,16,17,28,29,30,35,38,40,41,42,43,44,45,47,48,49,50,],[25,-12,-7,-28,-26,-27,-29,-30,-10,-11,-14,-15,-16,-1,-28,-12,-13,-19,-2,-3,25,-5,-6,25,-17,-20,-18,-21,]),'EQUAL':([3,],[26,]),'ARROW':([3,6,7,8,9,10,11,12,13,15,16,17,29,30,35,38,47,48,49,50,],[-12,31,-28,-26,-27,-29,-30,-10,-11,-14,-15,-16,-28,-12,-13,-19,-17,-20,-18,-21,]),'LPARENTHESES':([3,30,],[27,27,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'content':([0,18,19,20,27,],[1,36,37,39,46,]),'expr':([0,5,18,19,20,21,22,23,24,25,26,27,],[2,28,2,2,2,40,41,42,43,44,45,2,]),'setcontent':([0,7,18,19,20,27,32,],[4,33,4,4,4,4,33,]),'item':([0,5,18,19,20,21,22,23,24,25,26,27,31,],[6,6,6,6,6,6,6,6,6,6,6,6,47,]),'terminal':([0,5,7,18,19,20,21,22,23,24,25,26,27,31,32,],[7,29,32,7,7,7,29,29,29,29,29,29,7,29,32,]),'structure':([0,5,18,19,20,21,22,23,24,25,26,27,31,],[8,8,8,8,8,8,8,8,8,8,8,8,8,]),'macro':([0,5,18,19,20,21,22,23,24,25,26,27,31,],[9,9,9,9,9,9,9,9,9,9,9,9,9,]),'list':([0,5,18,19,20,21,22,23,24,25,26,27,31,],[10,10,10,10,10,10,10,10,10,10,10,10,10,]),'become':([0,5,18,19,20,21,22,23,24,25,26,27,31,],[11,11,11,11,11,11,11,11,11,11,11,11,11,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> content","S'",1,None,None,None),
  ('expr -> NOT expr','expr',2,'p_expr0','parser.py',22),
  ('expr -> expr MULT expr','expr',3,'p_expr2','parser.py',25),
  ('expr -> expr LSHIFT expr','expr',3,'p_expr4','parser.py',28),
  ('expr -> expr AND expr','expr',3,'p_expr6','parser.py',31),
  ('expr -> expr OR expr','expr',3,'p_expr8','parser.py',34),
  ('expr -> expr EQUIVALENT expr','expr',3,'p_expr10','parser.py',37),
  ('expr -> item','expr',1,'p_expr11','parser.py',40),
  ('setcontent -> terminal terminal','setcontent',2,'p_set0','parser.py',49),
  ('setcontent -> terminal setcontent','setcontent',2,'p_set1','parser.py',52),
  ('terminal -> STRING','terminal',1,'p_terminal0','parser.py',67),
  ('terminal -> INTEGER','terminal',1,'p_terminal1','parser.py',71),
  ('terminal -> ID','terminal',1,'p_terminal2','parser.py',75),
  ('terminal -> ADDROF ID','terminal',2,'p_terminal5','parser.py',79),
  ('terminal -> TIME','terminal',1,'p_terminal7','parser.py',83),
  ('terminal -> FLOAT','terminal',1,'p_terminal8','parser.py',87),
  ('terminal -> ELLIPSIS','terminal',1,'p_terminal9','parser.py',91),
  ('become -> item ARROW item','become',3,'p_become','parser.py',98),
  ('list -> LBRACKET content RBRACKET','list',3,'p_list0','parser.py',108),
  ('list -> LBRACKET RBRACKET','list',2,'p_list1','parser.py',113),
  ('structure -> LBRACE content RBRACE','structure',3,'p_structure','parser.py',122),
  ('macro -> ID LPARENTHESES content RPARENTHESES','macro',4,'p_macro','parser.py',136),
  ('content -> content COMMA content','content',3,'p_content2','parser.py',148),
  ('content -> expr','content',1,'p_content3','parser.py',152),
  ('content -> ID EQUAL expr','content',3,'p_content4','parser.py',156),
  ('content -> setcontent','content',1,'p_content5','parser.py',160),
  ('item -> structure','item',1,'p_item0','parser.py',174),
  ('item -> macro','item',1,'p_item1','parser.py',178),
  ('item -> terminal','item',1,'p_item2','parser.py',182),
  ('item -> list','item',1,'p_item3','parser.py',186),
  ('item -> become','item',1,'p_item5','parser.py',190),
]
