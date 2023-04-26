import sys
import ply.lex as lex
import ply.yacc as yacc

# Token Analysis

states = (
    ('state1','exclusive'), # need to find a better name 
    ('string','exclusive')
)

reserved = {
    'print': 'PRINT',
    'for': 'FOR',
    'in': 'IN',
    'do': 'DO',
    'endfor': 'ENDFOR'
}

literals = ['<', '>', '.', ',']

tokens = [
             'DUMBO_START',
             'DUMBO_END',
             'QUOTE',
             'ASSIGN',
             'ID',
             'TXT',
             'LPARENTHESE',
             'RPARENTHESE',
             'STRING',
             'SEMICOLON'
         ] + list(reserved.values())


# INITIAL STATE

def t_DUMBO_START(t) :
    r'(\{\{)'
    t.lexer.begin('state1')
    return t

def t_TXT(t):
    r'[^({{)]+'
    return t

t_ignore = ' \t \n'

# STATE 1

def t_state1_DUMBO_END(t):
    r'(\}\})'
    t.lexer.begin('INITIAL')
    return t

def t_state1_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_state1_QUOTE(t):
    r'\''
    t.lexer.begin('string')
    return t

def t_state1_ASSIGN(t):
    r':='
    return t

def t_state1_LPARENTHESE(t):
    r'\('
    return t

def t_state1_RPARENTHESE(t):
    r'\)'
    return t

def t_state1_SEMICOLON(t):
    r';'
    return t

t_state1_ignore = ' \t \n'


# STRING STATE

def t_string_STRING(t):
    r'[^\']+'
    return t

def t_string_QUOTE(t):
    r'\''
    t.lexer.begin('state1')
    return t



def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Syntaxical Analysis

# CONFLICT IN STATE 13 AND 28

dico = {}
temp_dico = {}

def p_programme_txt(p):
    '''programme : txt
                 | txt programme'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]
    print(13)

def p_programme_dumbo(p):
    '''programme : dumbo_bloc
                 | dumbo_bloc programme'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]
    print(12)

def p_txt(p):
    '''txt : TXT'''
    p[0] = p[1]
    print(11)

def p_dumbo_bloc(p):
    '''dumbo_bloc : DUMBO_START expression_list DUMBO_END'''
    if p[1] == '{{' and p[3] == '}}':
        p[0] = p[2]
    print(10)

def p_expression_list(p):
    '''expression_list : expression SEMICOLON expression_list
                       | expression SEMICOLON'''
    if len(p) == 3:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[1] + p[3]
    print(9)

def p_expression_print(p):
    '''expression : PRINT string_expression'''
    if len(p) == 3:
        p[0] = p[2]
    print(p[2])

def p_expression_for(p):
    '''expression : FOR variable IN string_list DO expression_list ENDFOR
                  | FOR variable IN variable DO expression_list ENDFOR'''
    if len(p) == 8:
        p[0] = ''
        for i in p[4]:
            temp_dico[p[2]] = i
            print(p[6])
            p[0] += p[6]
    print(7)

def p_expression_var(p):
    '''expression : variable ASSIGN string_expression
                  | variable ASSIGN string_list'''
    if len(p) == 4:
        dico[p[1]] = p[3]
        p[0] = ""
    print(6)

def p_string_expression(p):
    '''string_expression : string
                         | variable
                         | string_expression '.' string_expression '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[1] + p[3]
    print(5)

def p_string_list(p):
    '''string_list : LPARENTHESE string_list_interior RPARENTHESE '''
    if len(p) == 4:
        p[0] = p[2]
    print(4)

def p_string_list_interior(p):
    '''string_list_interior : string
                            | string ',' string_list_interior'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    print(3)


def p_variable(p):
    '''variable : ID'''
    if str(p[1]) in temp_dico:
        p[0] = temp_dico.get(str(p[1]))
    elif str(p[1]) in dico :
        p[0] = dico.get(str(p[1]))
    else :
        p[0] = p[1]
    print(2)

def p_string(p):
    '''string : QUOTE STRING QUOTE'''
    p[0] = p[2]
    print(p[2])


def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
        parser.errok()
    else:
        print("Syntax error at EOF")


# SEMANTIC ANALYSIS

#TO-DO


# Testing
if __name__ == "__main__":
    lexer = lex.lex()
    parser = yacc.yacc()

    dumbo = open(sys.argv[1]).read()
    yacc.parse(dumbo, debug=True)
    print("------------------------------------")
    print(dico.items())
    template = open(sys.argv[2]).read()
    result = yacc.parse(template, debug=True)
    print(result)
