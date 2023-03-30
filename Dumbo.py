import ply.lex as lex

#BRACKET et ANGLE_BRACKET réunis les 2 types pour le moment
tokens = (      
    'BRACKET',
    'PIPE',
    'ANGLE_BRACKET',
    'SLASH',
    'SEMICOLON',
    'COLON',
    'EQUAL',
    'QUOTE',
    'SINGLE_QUOTE',
    'HTML_TAG'
)


t_BRACKET = r'\{|\}'
t_PIPE = r'\|'
t_ANGLE_BRACKET = r'<|>'
t_SLASH = r'/'
t_SEMICOLON = r';'
t_COLON = r':'
t_EQUAL = r'='
t_QUOTE = r'\"'
t_SINGLE_QUOTE = r'\''


def t_HTML_TAG(t):
    r'html|head|title|body|h1|br'
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
