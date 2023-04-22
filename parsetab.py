
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "ASSIGN DO DUMBO_END DUMBO_START ENDFOR FOR ID IN LPARENTHESE PRINT QUOTE RPARENTHESE SEMICOLON STRING TXTprogramme : txt\n                 | txt programmeprogramme : dumbo_bloc\n                 | dumbo_bloc programmetxt : TXTdumbo_bloc : DUMBO_START expression_list DUMBO_ENDexpression_list : expression SEMICOLON expression_list\n                       | expression SEMICOLONexpression : ID string_expressionexpression : ID variable ID string_list ID expression_list ID\n                  | ID variable ID variable ID expression_list IDexpression : variable ASSIGN string_expression\n                  | variable ASSIGN string_liststring_expression : string\n                         | variable\n                         | string_expression '.' string_expression string_list : LPARENTHESE string_list_interior RPARENTHESE string_list_interior : string\n                            | string ',' string_list_interiorvariable : IDstring : QUOTE STRING QUOTE"
    
_lr_action_items = {'TXT':([0,2,3,4,12,],[4,4,4,-5,-6,]),'DUMBO_START':([0,2,3,4,12,],[5,5,5,-5,-6,]),'$end':([1,2,3,4,6,7,12,],[0,-1,-3,-5,-2,-4,-6,]),'ID':([5,10,13,14,16,19,20,21,22,29,30,34,35,36,38,39,],[10,14,10,-20,22,14,-7,14,14,34,35,10,10,-17,41,42,]),'DUMBO_END':([8,13,20,],[12,-8,-7,]),'SEMICOLON':([9,14,15,16,17,24,25,26,28,31,36,41,42,],[13,-20,-9,-15,-14,-15,-12,-13,-16,-21,-17,-11,-10,]),'ASSIGN':([10,11,],[-20,19,]),'QUOTE':([10,19,21,23,27,37,],[18,18,18,31,18,18,]),'.':([14,15,16,17,24,25,28,31,],[-20,21,-15,-14,-15,21,21,-21,]),'STRING':([18,],[23,]),'LPARENTHESE':([19,22,],[27,27,]),',':([31,33,],[-21,37,]),'RPARENTHESE':([31,32,33,40,],[-21,36,-18,-19,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'programme':([0,2,3,],[1,6,7,]),'txt':([0,2,3,],[2,2,2,]),'dumbo_bloc':([0,2,3,],[3,3,3,]),'expression_list':([5,13,34,35,],[8,20,38,39,]),'expression':([5,13,34,35,],[9,9,9,9,]),'variable':([5,10,13,19,21,22,34,35,],[11,16,11,24,24,29,11,11,]),'string_expression':([10,19,21,],[15,25,28,]),'string':([10,19,21,27,37,],[17,17,17,33,33,]),'string_list':([19,22,],[26,30,]),'string_list_interior':([27,37,],[32,40,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programme","S'",1,None,None,None),
  ('programme -> txt','programme',1,'p_programme_txt','Dumbo.py',112),
  ('programme -> txt programme','programme',2,'p_programme_txt','Dumbo.py',113),
  ('programme -> dumbo_bloc','programme',1,'p_programme_dumbo','Dumbo.py',121),
  ('programme -> dumbo_bloc programme','programme',2,'p_programme_dumbo','Dumbo.py',122),
  ('txt -> TXT','txt',1,'p_txt','Dumbo.py',130),
  ('dumbo_bloc -> DUMBO_START expression_list DUMBO_END','dumbo_bloc',3,'p_dumbo_bloc','Dumbo.py',135),
  ('expression_list -> expression SEMICOLON expression_list','expression_list',3,'p_expression_list','Dumbo.py',141),
  ('expression_list -> expression SEMICOLON','expression_list',2,'p_expression_list','Dumbo.py',142),
  ('expression -> ID string_expression','expression',2,'p_expression_print','Dumbo.py',150),
  ('expression -> ID variable ID string_list ID expression_list ID','expression',7,'p_expression_for','Dumbo.py',156),
  ('expression -> ID variable ID variable ID expression_list ID','expression',7,'p_expression_for','Dumbo.py',157),
  ('expression -> variable ASSIGN string_expression','expression',3,'p_expression_var','Dumbo.py',164),
  ('expression -> variable ASSIGN string_list','expression',3,'p_expression_var','Dumbo.py',165),
  ('string_expression -> string','string_expression',1,'p_string_expression','Dumbo.py',171),
  ('string_expression -> variable','string_expression',1,'p_string_expression','Dumbo.py',172),
  ('string_expression -> string_expression . string_expression','string_expression',3,'p_string_expression','Dumbo.py',173),
  ('string_list -> LPARENTHESE string_list_interior RPARENTHESE','string_list',3,'p_string_list','Dumbo.py',181),
  ('string_list_interior -> string','string_list_interior',1,'p_string_list_interior','Dumbo.py',187),
  ('string_list_interior -> string , string_list_interior','string_list_interior',3,'p_string_list_interior','Dumbo.py',188),
  ('variable -> ID','variable',1,'p_variable','Dumbo.py',196),
  ('string -> QUOTE STRING QUOTE','string',3,'p_string','Dumbo.py',201),
]
