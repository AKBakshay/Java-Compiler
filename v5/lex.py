# ----------------------------------------------------------------------
# Shashwat Ranjan Chaurasia
# 14641
# ----------------------------------------------------------------------
# ass1.py  
# tokeniser for Java8
# ----------------------------------------------------------------------


import ply.lex as lex
import sys

keyset 	= [ 'const'   ,   'float'   ,   'native'    ,   'super'   ,    'while' ,  'class' ,     'finally'  ,  'long'    ,     'strictfp'  ,  'volatile', 'char'   ,    'final'    ,  'interface' ,   'static'  ,    'void',  'catch'  ,    'extends'  ,  'int'    ,      'short'  ,     'try', 'case'  ,     'enum'   ,    'instanceof'  , 'return'   ,   'transient', 'byte'    ,   'else'   ,    'import'  ,     'public'  ,    'throws',   'boolean'  ,  'do'       ,  'goto'    ,     'private'  ,   'this', 'break'   ,   'double'   ,  'implements'  , 'protected'  , 'throw' , 'abstract'  , 'continue'  , 'for'       ,   'new'      ,   'switch',  'assert'  ,   'default' ,   'if'        ,   'package'  ,   'synchronized' ]

# listing all the tokens
tokens=[
		'Identifier',
		'Literal',
		'LAMBDAARROW',
		'DOUBLECOLON',
		'OR', 'AND', 'EQ', 'NEQ', 'GTEQ', 'LTEQ', 'LSHIFT', 'RSHIFT', 'RRSHIFT', 'TIMES_EQUAL', 'DIVIDE_EQUAL', 'REMAINDER_EQUAL',
		'PLUS_EQUAL', 'MINUS_EQUAL', 'LSHIFT_EQUAL', 'RSHIFT_EQUAL', 'RRSHIFT_EQUAL', 'AND_EQUAL', 'XOR_EQUAL', 'OR_EQUAL',
		'PLUSPLUS', 'MINUSMINUS', 'ELLIPSIS', 'DOT'

	] + [x for x in keyset]

literals = '[](){}<>+-*/=?@%~&:;,^|!'


t_LAMBDAARROW = '->'
t_DOUBLECOLON = '::'
t_OR = r'\|\|'
t_AND = '&&'

t_EQ = '=='
t_NEQ = '!='
t_GTEQ = '>='
t_LTEQ = '<='

t_LSHIFT = '<<'
t_RSHIFT = '>>'
t_RRSHIFT = '>>>'

t_TIMES_EQUAL = r'\*='
t_DIVIDE_EQUAL = '/='
t_REMAINDER_EQUAL = '%='
t_PLUS_EQUAL = r'\+='
t_MINUS_EQUAL = '-='
t_LSHIFT_EQUAL = '<<='
t_RSHIFT_EQUAL = '>>='
t_RRSHIFT_EQUAL = '>>>='
t_AND_EQUAL = '&='
t_XOR_EQUAL = '\^='
t_OR_EQUAL = r'\|='

t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'\-\-'

t_ELLIPSIS = r'\.\.\.'
t_DOT= '.'

t_ignore = ' \f\t'


# def t_ignore_my(t):
# 	r' | \t| \f'
# 	pass

def t_ignore_comment_singleline(t):
	r'//.*'


def t_ignore_comment_multiline(t):
	r'/\*(\r\n|\r|\n|.)*?\*/'
	# if(t.value=='.'):
	# 	print ("yaha galat hai ")
	# t.value
	t.lexer.lineno += t.value.count('\n\r')
	t.value = ' '.join(re.split('\r\n', t.value))
	t.lexer.lineno += t.value.count('\n')
	t.lexer.lineno += t.value.count('\r')
	


def t_nan(t):
	r'\bFloat.NaN\b|\bDouble.NaN\b'
	t.type	= 'Literal'
	return t

# Defining the tokens using regualar expressions



def t_KEYWORD(t):
	r'[a-zA-Z_$][a-zA-Z0-9_$]*'
	if t.value in keyset:
		t.type 	= t.value 
	elif t.value in ['true', 'false', 'null', 'POSITIVE_INFINITY', 'NEGATIVE_INFINITY']:
		t.type	= 'Literal'
	else:
		t.type	= 'Identifier'
	return t



def t_flh(t): #float hexadecimal
	r'0[xX][0-9a-fA-F]([0-9a-fA-F_]*[0-9a-fA-F]+)*(\.)?([0-9a-fA-F]([0-9a-fA-F_]*[0-9a-fA-F]+)*)?[pP][-+]?[0-9]([0-9_]*[0-9]+)*[fFdD]?|0[xX]([0-9a-fA-F]([0-9a-fA-F_]*[0-9a-fA-F]+)*)?(\.)?[0-9a-fA-F]([0-9a-fA-F_]*[0-9a-fA-F]+)*[pP][-+]?[0-9]([0-9_]*[0-9]+)*[fFdD]?'
	t.type	= 'Literal'
	return t

def t_hex(t): #hex integer literal
	r'0[xX][0-9a-fA-F]([0-9a-fA-F_]*[0-9a-fA-F]+)*[lL]?'
	t.type	= 'Literal'
	return t

def t_bin(t): #bin integer literal
	r'0[bB][0-1]([0-1_]*[0-1]+)*[lL]?'
	t.type	= 'Literal'
	return t

def t_fld(t): #float decimal
	r'[+-]?[0-9]([0-9_]*[0-9]+)*[lL]|[-+]?[0-9]([0-9_]*[0-9]+)*(\.)?([0-9]([0-9_]*[0-9]+)*)?([eE][-+]?[0-9]([0-9_]*[0-9]+)*)?[fFdD]?|[-+]?([0-9]([0-9_]*[0-9]+)*)?(\.)?[0-9]([0-9_]*[0-9]+)*([eE][-+]?[0-9]([0-9_]*[0-9]+)*)?[fFdD]?'
	t.type	= 'Literal'
	return t

def t_oct(t): #oct integer literal
	r'0([0-7_]*[0-7]+)+[lL]?'
	t.type	= 'Literal'
	return t

def t_dec(t): #decimal integer literal
	r'[0-9]([0-9_]*[0-9]+)*[lL]?'
	t.type	= 'Literal'
	return t


# -------------------------------------------------------------------------
def t_str(t):
	r'"([^\n\r"\\]?(\\r)?(\\\')?(\\t)?(\\")?(\\n)?(\\\\)?(\\b)?(\\f)?|\\[0-3][0-7][0-7]|\\[0-7][0-7]|\\[0-7])*"'
	t.type	= 'Literal'
	return t


# ----------------------------------------------------------------------------

def t_chr(t):
    r'\'([^\r\n\t\f"\'\\]|\\r|\\\'|\\t|\\"|\\n|\\\\|\\b|\\f|\\[0-3][0-7][0-7]|\\[0-7][0-7]|\\[0-7])\''
    t.type	= 'Literal'
    return t



# -------------------------------------------------------------------------

# def t_OPERATOR(t):
# 	# r'==|>=|<=|!=|&&|\|\||\+\+|--|\+=|-=|\*=|/=|&=|\|=|\^=|%=|<<=|>>>=|>>=|->|\+|-|\*|/|&|\||\^|%|<<|>>>|>>|=|>|<|!|~|\?|:'
# 	r'==|>=|<=|!=|&&|\|\||\+\+|--|\+=|-=|\*=|/=|&=|\|=|\^=|%=|<<=|>>>=|>>=|->|\+|-|\*|/|&|\||\^|%|<<|=|>|<|!|~|\?|:'
# 	return t



# for counting the lines
def t_lineterminator(t):
	r'(\r\n)'
	t.lexer.lineno += 1

def t_newline(t):
    r'\n+|\r+'
    t.lexer.lineno += len(t.value)


# for error handling
def t_error(t):
    # print("Not a legal character Bro '%s' on line number '%i'" % t.value[0], % t.lexer.lineno)
    print ('Illegal Character {} on line number {}'.format(t.value[0], t.lexer.lineno))
    t.lexer.skip(1)

# -------------------------------------------------------------------------------------------------------------------------------------


lexer = lex.lex()


