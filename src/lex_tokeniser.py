import sys 

tokens = (
    'ignore',
    'comment',
    'newline',
    'Keyword',
    'EXCASE',
    'Literal',
    'Identifier',
    'Separator',
    'Operator',
    'String',
    'EOF'
)

t_ignore  = ' \t\f'


#------------------Literals----------------------------------

def t_EOF(t):
    r'<EOF>'
    return t

def t_HEXADEC(t):
    r'0[xX][0-9a-fA-F]([0-9a-fA-F_]*[0-9a-fA-F])?\.?([0-9a-fA-F]([0-9a-fA-F_]*[0-9a-fA-F])?)?[pP][+-]?[0-9]([0-9_]*[0-9])?[fFdD]?|0[xX]([0-9a-fA-F]([0-9a-fA-F_]*[0-9a-fA-F])?)?\.[0-9a-fA-F]([0-9a-fA-F_]*[0-9a-fA-F])?[pP][+-]?[0-9]([0-9_]*[0-9])?[fFdD]?'
    t.type = 'Literal'
    return t

def t_HEXA(t):
    r'0[xX][0-9a-fA-F]([0-9a-fA-F_]*[0-9a-fA-F])?[lL]?'
    t.type = 'Literal'
    return t


def t_BINARY(t):
    r'0[bB][01]([01_]*[01])?[lL]?'
    t.type = 'Literal'
    return t

def t_FLOAT_INT(t):
    r'[0-9]([0-9_]*[0-9])?[lL]|[0-9]([0-9_]*[0-9])?(\.)?([0-9]([0-9_]*[0-9])?)?([eE][+-]?[0-9]([0-9_]*[0-9])?)?[fFdD]?|([0-9]([0-9_]*[0-9])?)?(\.)?[0-9]([0-9_]*[0-9])?([eE][+-]?[0-9]([0-9_]*[0-9])?)?[fFdD]?'
    t.type = 'Literal'
    return t

def t_STRING(t):
    r'"(\\[0-3]?[0-7]?[0-7]|[^\r\n"\\]?(\\b)?(\\t)?(\\n)?(\\f)?(\\r)?(\\")?(\\\')?(\\\\)?)*"|\'(\\[0-3]?[0-7]?[0-7]|[^\r\n\t\f"\'\\]|(\\b)|(\\t)|(\\n)|(\\f)|(\\r)|(\\")|(\\\')|(\\\\))\''
    t.type = 'String'
    return t
 

#---------------------------------------------------------


def t_comment(t):
    r'/\*(.|\n|\r|\r\n)*?\*/|//.*'
    t.lexer.lineno += t.value.count('\r\n')
    t.lexer.lineno += t.value.count('\r') - t.value.count('\r\n')
    t.lexer.lineno += t.value.count('\n') - t.value.count('\r\n')
    pass                       

def t_Keyword(t): 
    r'\babstract\b|\bcontinue\b|\bfor\b|\bnew\b|\bswitch\b|\bassert\b|\bdefault\b|\bif\b|\bpackage\b|\bsynchronized\b|\bboolean\b|\bdo\b|\bgoto\b|\bprivate\b|\bthis\b|\bbreak\b|\bdouble\b|\bimplements\b|\bprotected\b|\bthrow\b|\bbyte\b|\belse\b|\bimport\b|\bpublic\b|\bthrows\b|\bcase\b|\benum\b|\binstanceof\b|\breturn\b|\btransient\b|\bcatch\b|\bextends\b|\bint\b|\bshort\b|\btry\b|\bchar\b|\bfinal\b|\binterface\b|\bstatic\b|\bvoid\b|\bclass\b|\bfinally\b|\blong\b|\bstrictfp\b|\bvolatile\b|\bconst\b|\bfloat\b|\bnative\b|\bsuper\b|\bwhile\b'
    return t

def t_EXCASE(t):
    r'[a-zA-Z_$][\w$]*[ \t]*(((,[ \t]*[a-zA-Z_$][\w$]*[ \t]*)*<[ \t]*[a-zA-Z_$][\w$]*[ \t]*(,[ \t]*[a-zA-Z_$][\w$]*[ \t]*)*)|((,[ \t]*[a-zA-Z_$][\w$]*[ \t]*)*>[ \t]*))+[ \t]*'
    return t

def t_Literal(t):
    r'\bPOSITIVE_INFINITY\b|\bNEGATIVE_INFINITY\b|\bFloat\.NaN\b|\bDouble.NaN\b|\bnull\b|\btrue\b|\bfalse\b|[0-9][0-9_]*.[0-9_]*[0-9]e[+-]?[0-9]([0-9_]*[0-9])?[fFdD]|[0-9a-fA-F][0-9a-fA-F_]*.[0-9a-fA-F_]*[0-9a-fA-F][pP][+-][0-9a-fA-F]([0-9a-fA-F_]*[0-9a-fA-F])?|[0-9]([0-9_]*[0-9])?[lL]?|0x[0-9a-fA-F]([0-9a-fA-F_]*[0-9a-fA-F])?|[0-7]([0-7_]*[0-7])?|0[bB][01]([01_]*[01])?'
    return t

def t_newline(t):
    r'\r\n|\n|\r'
    t.lexer.lineno += 1


def t_Identifier(t):
    r'\b[a-zA-Z_$][\w$]*\b'         
    return t

def t_Separator(t):
    r'\(|\)|\{|\}|\[|\]|;|,|\.\.\.|\.|@|::'
    return t

def t_Operator(t):
    r'>>>=|>>=|<<=|\+=|-=|\*=|/=|&=|\|=|\^=|%=|<<|>>|->|==|>=|<=|!=|&&|\|\||\+\+|--|=|>|<|!|~|\?|:|\+|-|\*|/|&|\||\^|%'
    return t


def t_error(t):
    print("Illegal character '{}' in line {}".format(t.value[0], t.lexer.lineno))
    print("Lexical Analysis Terminating")
    sys.exit()
