import ply.lex as lex


tokens = (      
    'DUMBO_MARK',
    'SEMICOLON',
    'ASSIGN',
    'TXT'
)

#Tokens defined by strings are added by sorting them in order of
#decreasing regular expression length (longer expressions are added first).
t_DUMBO_MARK = r'(\{\{)|(\}\})'
t_SEMICOLON = r';'
t_ASSIGN = r':='


def t_TXT(t):
    r'(\w|\W|[^\S])*'
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
    lexer.input("{|} |}<  >/ ;; := \" \'")
    for token in lex.lexer:
        print("line %d : %s (%s)" % (token.lineno, token.type, token.value))
