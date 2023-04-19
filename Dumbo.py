import ply.lex as lex
import ply.yacc as yacc

# Token Analysis


reserved = {
    'print': 'PRINT',
    'for': 'FOR',
    'in': 'IN',
    'do': 'DO',
    'endfor': 'ENDFOR'
}

literals = ['<', '>', ';']

tokens = [
             'DUMBO_MARK',
             'ASSIGN',
             'LETTERS',
             'NUMBERS',
             'SYMBOLS',
             'SYMBOLS_NO_BRACKETS',
             'ID',
             'TXT'
             'STRING'
             'VARIABLE'
         ] + list(reserved.values())

# Tokens defined by strings are added by sorting them in order of
# decreasing regular expression length (longer expressions are added first).
t_DUMBO_MARK = r'(\{\{)|(\}\})'
t_LETTERS = r'[a-zA-Z]'
t_NUMBERS = r'\d'
t_SYMBOLS = r'\W'
t_SYMBOLS_NO_BRACKETS = r'[^a-zA-Z0-9{}]'
t_TXT = r'[^{]+'
t_STRING = r'.*'  # The correct expression is '.*', not only .*
t_VARIABLE = r'[^0-9]\w+'


# All tokens defined by functions are added first in the same order as
# they appear in the lexer file
def t_ASSIGN(t):
    r':='
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.value = float(t.value)
    return t


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


t_ignore = ' \t'


# Syntaxical Analysis

def p_programme_txt(p):
    '''programme : txt
                 | txt programme'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]


def p_programme_dumbo(p):
    '''programme : dumbo_bloc
                 | dumbo_bloc programme'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]


def p_txt(p):
    '''txt : TXT'''
    p[0] = p[1]


def p_dumbo_bloc(p):
    '''dumbo_bloc : DUMBO_MARK expression_list DUMBO_MARK'''
    if p[1] == '{{' and p[3] == '}}':
        p[0] = p[2]


def p_expression_list(p):
    '''expression_list : expression ';' expression_list
                       | expression ';' '''
    if len(p) == 3:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[1] + p[3]


def p_expression_print(p):
    '''expression : ID string_expression'''
    if p[1] == 'print':
        p[0] = p[2]


def p_expression_for(p):
    '''expression : ID variable ID string_list ID expression_list ID
                  | ID variable ID variable ID expression_list ID'''
    if p[1] == 'for' and p[3] == 'in' and p[5] == 'do' and p[7] == 'endfor':
        for p[2] in p[4]:
            p[0] += p[6]


def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
        parser.errok()
    else:
        print("Syntax error at EOF")


def p_string_expression(p):
    '''string_expression : string
                         | variable
                         | string_expression.string_expression'''

    if p[1] == 'string':
        p[0] = p[1]
    elif p[1] == 'variable':
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]


def p_string_list(p):
    '''  string_list: string_list_interior'''
    if p[1] == 'string_list_interior':
        p_string_list_interior(p)


def p_string_list_interior(p):
    '''string_list_interior : string
                            | string ',' string_list_interior'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[3]


def p_variable(p):
    '''variable : VARIABLE'''
    p[0] = p[1]


def p_string(p):
    '''string : STRING'''
    p[0] = p[1]


# Testing
if __name__ == "__main__":
    lexer = lex.lex()
    parser = yacc.yacc()
    result = yacc.parse("string", debug=True)
    print(result)
