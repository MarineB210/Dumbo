import sys
from ply import lex
from ply import yacc


# TOKEN ANALYSIS

states = (
    ('bloc', 'exclusive'),
    ('string', 'exclusive')
)

reserved = {
    'print': 'PRINT',
    'for': 'FOR',
    'in': 'IN',
    'do': 'DO',
    'endfor': 'ENDFOR',
    'and': 'AND',
    'or': 'OR',
    'if': 'IF',
    'endif': 'ENDIF'
}

literals = ['<', '>', '.', ',', '=']

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
             'SEMICOLON',
             'OP',
             'DIFF',
             'INTEGER'
         ] + list(reserved.values())


# INITIAL STATE


def t_DUMBO_START(t):
    r'(\{\{)'
    t.lexer.begin('bloc')
    return t


def t_TXT(t):
    r'[^{]+'
    return t


# BLOC STATE

def t_bloc_DUMBO_END(t):
    r'(\}\})'
    t.lexer.begin('INITIAL')
    return t


def t_bloc_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_bloc_INTEGER(t):
    r'-?(0|([1-9])+)'
    t.value = int(t.value)
    return t


def t_bloc_OP(t):
    r'\+|-|\*|/'
    return t


def t_bloc_QUOTE(t):
    r'\''
    t.lexer.begin('string')
    return t


def t_bloc_ASSIGN(t):
    r':='
    return t


def t_bloc_DIFF(t):
    r'!='
    return t


def t_bloc_LPARENTHESE(t):
    r'\('
    return t


def t_bloc_RPARENTHESE(t):
    r'\)'
    return t


def t_bloc_SEMICOLON(t):
    r';'
    return t


t_bloc_ignore = ' \t \n'


# STRING STATE

def t_string_STRING(t):
    r'[^\']+'
    return t


def t_string_QUOTE(t):
    r'\''
    t.lexer.begin('bloc')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# ------------------------------------------------------------
# SYNTAXICAL ANALYSIS

dico = {}


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
    '''dumbo_bloc : DUMBO_START expression_list DUMBO_END
                  | DUMBO_START DUMBO_END'''
    if len(p) == 4:
        p[0] = p[2].do()
    else:
        p[0] = ''


def p_expression_list(p):
    '''expression_list : expression SEMICOLON expression_list
                       | expression SEMICOLON'''
    if len(p) == 3:
        p[0] = ExpressionList(p[1])
    elif len(p) == 4:
        p[0] = ExpressionList(p[1], p[3])


def p_expression_print(p):
    '''expression : PRINT string_expression'''
    if len(p) == 3:
        p[0] = Print(p[2])


def p_expression_for(p):
    '''expression : FOR variable IN string_list DO expression_list ENDFOR
                  | FOR variable IN variable DO expression_list ENDFOR'''
    if len(p) == 8:
        p[0] = For(p[2], p[4], p[6])


def p_expression_if(p):
    '''expression : IF boolean_op DO expression_list ENDIF
                  | IF comparison DO expression_list ENDIF'''
    p[0] = If(p[2], p[4])


def p_expression_var(p):
    '''expression : variable ASSIGN string_expression
                  | variable ASSIGN string_list
                  | variable ASSIGN integer'''
    if len(p) == 4:
        p[0] = Assign(p[1], p[3])


def p_string_expression(p):
    '''string_expression : string
                         | variable
                         | string '.' string_expression
                         | variable '.' string_expression '''
    if len(p) == 2:
        p[0] = StringExpression(p[1])
    elif len(p) == 4:
        p[0] = StringExpression(p[1], p[3])


def p_string_list(p):
    '''string_list : LPARENTHESE string_list_interior RPARENTHESE '''
    if len(p) == 4:
        p[0] = StringList(p[2])


def p_string_list_interior(p):
    '''string_list_interior : string
                            | string ',' string_list_interior'''
    if len(p) == 2:
        p[0] = StringListInterior(p[1])
    elif len(p) == 4:
        p[0] = StringListInterior(p[1], p[3])


def p_variable(p):
    '''variable : ID'''
    p[0] = Variable(p[1])


def p_string(p):
    '''string : QUOTE STRING QUOTE'''
    p[0] = Str(p[2])


def p_arithmetic_variable(p):
    '''arithmetic : variable OP variable'''
    p[0] = OperationVariable(p[2], p[1], p[3])


def p_arithmetic_var_ar(p):
    '''arithmetic : variable OP INTEGER'''
    p[0] = OperationVarInt(p[2], p[1], p[3])


def p_arithmetic_ar_var(p):
    '''arithmetic : INTEGER OP variable'''
    p[0] = OperationVarInt(p[2], p[3], p[1])


def p_arithmetic_ar(p):
    '''arithmetic : INTEGER OP INTEGER'''
    p[0] = OperationInt(p[2], p[1], p[3])


def p_integer(p):
    '''integer : arithmetic
               | INTEGER'''
    p[0] = Integer(p[1])


def p_boolean_op(p):
    '''boolean_op : comparison OR comparison
                  | comparison AND comparison
                  | boolean_op AND comparison
                  | boolean_op OR comparison'''
    p[0] = BooleanOp(p[1], p[2], p[3])


def p_comparison(p):
    '''comparison : integer '<' integer
                  | integer '>' integer
                  | integer '=' integer
                  | integer DIFF integer'''
    p[0] = Comparison(p[1], p[2], p[3])


def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
        parser.errok()
    else:
        print("Syntax error at EOF")

# ------------------------------------------------------------
# SEMANTIC ANALYSIS


class For:
    def __init__(self, var, args, expr):
        self.var = var
        self.args = args
        self.expr = expr

    def do(self):
        p = ''
        value = dico.get(self.var.get_name())
        for i in self.args.get_value():
            dico[self.var.get_name()] = i
            p += self.expr.do()
        if value is not None:
            dico[self.var.get_name()] = value
        else:
            del dico[self.var.get_name()]
        return p


class Print:
    def __init__(self, exp):
        self.exp = exp

    def do(self):
        return str(self.exp.do())


class If:
    def __init__(self, boolean, expr):
        self.boolean = boolean
        self.expr = expr

    def do(self):
        if self.boolean.do():
            return self.expr.do()
        return ''


class Variable:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.type = 'variable'

    def get_value(self):
        return dico.get(self.name)

    def get_name(self):
        return self.name


class Integer:
    def __init__(self, value):
        self.value = value

    def do(self):
        if isinstance(self.value, int):
            return self.value
        return self.value.do()


class Str:
    def __init__(self, value):
        self.value = value
        self.type = 'string'

    def get_value(self):
        return self.value


class OperationVariable:
    def __init__(self, op, value1, value2):
        self.value1 = value1
        self.value2 = value2
        self.op = op

    def do(self):
        match self.op:
            case '+':
                return self.value1.get_value() + self.value2.get_value()
            case '-':
                return self.value1.get_value() - self.value2.get_value()
            case '*':
                return self.value1.get_value() * self.value2.get_value()
            case '/':
                return self.value1.get_value() / self.value2.get_value()


class OperationVarInt:
    def __init__(self, op, var, integer):
        self.op = op
        self.var = var
        self.integer = integer

    def do(self):
        match self.op:
            case '+':
                return self.var.get_value() + self.integer
            case '-':
                return self.var.get_value() - self.integer
            case '*':
                return self.var.get_value() * self.integer
            case '/':
                return self.var.get_value() / self.integer


class OperationInt:
    def __init__(self, op, integer1, integer2):
        self.op = op
        self.integer1 = integer1
        self.integer2 = integer2

    def do(self):
        match self.op:
            case '+':
                return self.integer1 + self.integer2
            case '-':
                return self.integer1 - self.integer2
            case '*':
                return self.integer1 * self.integer2
            case '/':
                return self.integer1 / self.integer2


class BooleanOp:
    def __init__(self, value1, op, value2):
        self.value1 = value1
        self.op = op
        self.value2 = value2

    def do(self):
        if self.op == 'and':
            return self.value1.do() and self.value2.do()
        return self.value1.do() or self.value2.do()


class Comparison:
    def __init__(self, value1, op, value2):
        self.value1 = value1
        self.value2 = value2
        self.op = op

    def do(self):
        match self.op:
            case '<':
                return self.value1.do() < self.value2.do()
            case '>':
                return self.value1.do() > self.value2.do()
            case '=':
                return self.value1.do() == self.value2.do()
            case '!=':
                return self.value1.do() != self.value2.do()


class StringListInterior:
    def __init__(self, string, string_list_interior=None):
        self.string = string
        self.string_list_interior = string_list_interior

    def do(self):
        if self.string_list_interior is None:
            return [self.string.get_value()]
        return [self.string.get_value()] + self.string_list_interior.do()


class StringList:
    def __init__(self, string_list_interior):
        self.string_list_interior = string_list_interior
        self.type = 'string_list'

    def do(self):
        return self.string_list_interior.do()


class StringExpression:
    def __init__(self, expr, string_expression=None):
        self.expr = expr
        self.string_expression = string_expression
        self.type = 'string_expression'

    def do(self):
        if self.string_expression is None:
            return self.expr.get_value()
        else:
            return self.expr.get_value() + self.string_expression.do()


class Assign:
    def __init__(self, variable, string):
        self.variable = variable
        self.string = string

    def do(self):
        dico[self.variable.get_name()] = self.string.do()
        return ''


class ExpressionList:
    def __init__(self, expr1, expr2=None):
        self.expr1 = expr1
        self.expr2 = expr2

    def do(self):
        if self.expr2 is None:
            return self.expr1.do()
        return self.expr1.do() + self.expr2.do()


# ------------------------------------------------------------
# TESTING
if __name__ == "__main__":
    lexer = lex.lex()
    parser = yacc.yacc()

    dumbo = open(sys.argv[1], encoding='utf-8').read()
    yacc.parse(dumbo)

    template = open(sys.argv[2], encoding='utf-8').read()
    result = yacc.parse(template)

    file_html = open('output.html', 'w', encoding='utf-8')
    file_html.write(result)
    print(result)
