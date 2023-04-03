import ply.lex as lex
import ply.yacc as yacc

reserved = {
    'print': 'PRINT',
    'for': 'FOR',
    'in': 'IN',
    'do': 'DO',
    'endfor': 'ENDFOR'
}

tokens = [      
    'DUMBO_MARK',
    'SEMICOLON',
    'ASSIGN',
    'LETTERS',
    'NUMBERS',
    'SYMBOLS',
    'SYMBOLS_NO_BRACKETS',
    'ID'
] + list(reserved.values())

#Tokens defined by strings are added by sorting them in order of
#decreasing regular expression length (longer expressions are added first).
t_DUMBO_MARK = r'(\{\{)|(\}\})'
t_SEMICOLON = r';'
t_LETTERS = r'[a-zA-Z]'
t_NUMBERS = r'\d'
t_SYMBOLS = r'\W'
t_SYMBOLS_NO_BRACKETS = r'[^a-zA-Z0-9{}]'  #Might replace that one with a regex for simple brackets

#All tokens defined by functions are added first in the same order as 
#they appear in the lexer file
def t_ASSIGN(t):
    r':='
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*' #To change
    t.type = reserved.get(t.value, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.value = float(t.value)
    return t


def t_error(t):
    print("Illegalcharacter'%s" %t.value[0])
    t.lexer.skipe(1)


t_ignore = ' \t'


#Testing
if __name__ == "__main__":
    lexer = lex.lex()
    lexer.input("{|}print print {{ }} |}<  >/ ;; := \" \'")
    for token in lex.lexer:
        print("line %d : %s (%s)" % (token.lineno, token.type, token.value))
