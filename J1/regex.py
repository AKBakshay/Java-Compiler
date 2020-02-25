# This file defines the regular expressions to capture the tokens in token.py

from token_file import *
import sys
#Basic 
t_ignore 	= ' \t'
#t_COMMENT	= r'(\/\*(.|\n|\r)*?\*\/)|(\/\/.*?)'

#List of Operators. Are checked in the longest to shortest fashion, precedence over functions????

t_EQ 		=  r'\='
t_GRTHAN 	=  r'\>'
t_LETHAN 	=  r'\<'
t_EXCLAIM	=  r'\!'	
t_TILDE		=  r'\~'
t_QMARK		=  r'\?'
t_COLON		=  r'\:'
t_ARROW		=  r'\-\>'
t_DEQ 		=  r'\=\='
t_GREQ		=  r'\>\='
t_LEEQ		=  r'\<\='
t_NTEQ		=  r'\!\='
t_DAND		=  r'\&\&'
t_DOR		=  r'\|\|'
t_DPLUS		=  r'\+\+'
t_DMINUS	=  r'\-\-'
t_PLUS 		=  r'\+'
t_MINUS 	=  r'\-'
t_STAR 		=  r'\*'
t_FSLASH 	=  r'\/'
t_AND 		=  r'\&'
t_OR 		=  r'\|'
t_XOR  		=  r'\^'
t_MOD 		=  r'\%'
t_LSHIFT 	=  r'\<\<'
t_RSHIFT 	=  r'\>\>'
t_URSHIFT 	=  r'\>\>\>'
t_PLUSEQ 	=  r'\+\='
t_MINUSEQ 	=  r'\-\='
t_STAREQ 	=  r'\*\='
t_FSLASHEQ 	=  r'\/\='
t_ANDEQ 	=  r'\&\='
t_OREQ 		=  r'\|\='
t_XOREQ 	=  r'\^\='
t_MODEQ 	=  r'\%\='
t_LSHIFTEQ 	=  r'\<\<\='
t_RSHIFTEQ 	=  r'\>\>\='
t_URSHIFTEQ	=  r'\>\>\>\='

#List of separators

t_LPAR		=  r'\('
t_RPAR		=  r'\)'
t_LCURL		=  r'\{'
t_RCURL		=  r'\}'
t_LSQR		=  r'\['
t_RSQR		=  r'\]'
t_SCOLON	=  r'\;'
t_COMMA		=  r'\,'
t_POINT		=  r'\.'
t_VARARGS	=  r'\.\.\.'
t_ATRATE	=  r'\@'
t_MTREF		=  r'\:\:'

#Functions for identifiers, int, long, float, double, char, string
#reserved are handled with identifiers
#null, false, true are included in reserved
#doesn't handle unicode


def t_FLOATVAL(t):
	r'(0(x|X)(((([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?)?\.([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?((p|P)(\+|-)?([0-9])(([0-9]|\_)*([0-9]))?)?)|(([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?\.(([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?)?((p|P)(\+|-)?([0-9])(([0-9]|\_)*([0-9]))?)?)|(([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?(p|P)(\+|-)?([0-9])(([0-9]|\_)*([0-9]))?))(f|F))|(([0-9](([0-9]|\_)*[0-9])?\.([0-9](([0-9]|\_)*[0-9])?)?((e|E)(\+|-)?[0-9](([0-9]|\_)*[0-9])?)?(f|F))|(([0-9](([0-9]|\_)*[0-9])?)?\.[0-9](([0-9]|\_)*[0-9])?((e|E)(\+|-)?[0-9](([0-9]|\_)*[0-9])?)?(f|F))|([0-9](([0-9]|\_)*[0-9])?((e|E)(\+|-)?[0-9](([0-9]|\_)*[0-9])?)?(f|F)))'
	return t

def t_DOUBLEVAL(t):
	r'(0(x|X)(((([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?)?\.([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?((p|P)(\+|-)?([0-9])(([0-9]|\_)*[0-9])?)?)|(([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?\.(([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?)?((p|P)(\+|-)?([0-9])(([0-9]|\_)*[0-9])?)?)|(([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?(p|P)(\+|-)?[0-9](([0-9]|\_)*[0-9])?))(d|D)?)|(([0-9](([0-9]|\_)*[0-9])?\.([0-9](([0-9]|\_)*[0-9])?)?((e|E)(\+|-)?[0-9](([0-9]|\_)*[0-9])?)?(d|D)?)|(([0-9](([0-9]|\_)*[0-9])?)?\.[0-9](([0-9]|\_)*[0-9])?((e|E)(\+|-)?[0-9](([0-9]|\_)*[0-9])?)?(d|D)?)|([0-9](([0-9]|\_)*[0-9])?((e|E)(\+|-)?[0-9](([0-9]|\_)*[0-9])?)(d|D)?))'
	return t

def t_LONGVAL(t):
	r'(0(x|X)([A-F]|[a-f]|[0-9])(([A-F]|[a-f]|[0-9]|[\_])*([A-F]|[a-f]|[0-9]))?(l|L))|(0(b|B)([0-1])(([0-1]|[\_])*([0-1]))?(l|L))|(0(([0-7]|\_)*[0-7])?(l|L)|[1-9](([0-9]|\_)*[0-9])?(l|L))'
	#may check for value of long and return its value
	return t
def t_INTVAL(t):
	r'(0(x|X)([A-F]|[a-f]|[0-9])(([A-F]|[a-f]|[0-9]|[\_])*([A-F]|[a-f]|[0-9]))?)|(0(b|B)([0-1])(([0-1]|[\_])*([0-1]))?)|(0(([0-7]|\_)*[0-7])?|[1-9](([0-9]|\_)*[0-9])?)'
	#may check for value of integer later and return its value
	return t

def t_CHARVAL(t):
	r'(\'\\(b|t|n|f|r|"|\'|\\|[0-3][0-7][0-7]|[0-7][0-7]|[0-7])\')|(\'([\ -\&]|[\(-\[]|[\]-~])\')'
	return t

def t_STRINGVAL(t):
	r'\"(([ -\[]|[\]-~]|(\\(b|t|n|f|r|\"|\'|\\|[0-3][0-7][0-7]|[0-7][0-7]|[0-7])))*?)\"'
	return t

def t_COMMENT(t):
	r'(\/\*(.|\n|\r)*?\*\/)|(\/\/.*)'
	t.lexer.lineno += str(t.value).count('\n')
	return t

def t_IDENTIFIER(t):
	r'([A-Z]|[a-z]|\_|\$)([A-Z]|[a-z]|\_|\$|[0-9])*'
	t.type = reserved.get(t.value,'IDENTIFIER')
	return t



#newline and error stuff

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal Input: "+str(t.value)+" at line number: "+str(t.lineno))
    sys.exit()
    quit
    
    #Can do the below if you want to continue any further
    #t.lexer.skip(1)



# DO NOT DISTURB THESE STRINGS PLEASE. THEY WILL SERVE AS PARTS OF FLOAT etc in case of some errors

#intfloat = r'(([0-9](([0-9]|\_)*[0-9])?\.([0-9](([0-9]|\_)*[0-9])?)?((e|E)(\+|-)?[0-9](([0-9]|\_)*[0-9])?)?(f|F))|(([0-9](([0-9]|\_)*[0-9])?)?\.[0-9](([0-9]|\_)*[0-9])?((e|E)(\+|-)?[0-9](([0-9]|\_)*[0-9])?)?(f|F))|([0-9](([0-9]|\_)*[0-9])?((e|E)(\+|-)?[0-9](([0-9]|\_)*[0-9])?)?(f|F)))'
#hexfloat = r'((((([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?)?\.([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?(p|P)(\+|-)?([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?)|(([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?\.(([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?)?(p|P)(\+|-)?([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?)|(([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?(p|P)(\+|-)?([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?))(f|F))'
#intdouble = r'(([0-9](([0-9]|\_)*[0-9])?\.([0-9](([0-9]|\_)*[0-9])?)?((e|E)(\+|-)?[0-9](([0-9]|\_)*[0-9])?)?(d|D)?)|(([0-9](([0-9]|\_)*[0-9])?)?\.[0-9](([0-9]|\_)*[0-9])?((e|E)(\+|-)?[0-9](([0-9]|\_)*[0-9])?)?(d|D)?)|([0-9](([0-9]|\_)*[0-9])?((e|E)(\+|-)?[0-9](([0-9]|\_)*[0-9])?)?(d|D)?))'
#hexfloat = r'((((([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?)?\.([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?(p|P)(\+|-)?([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?)|(([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?\.(([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?)?(p|P)(\+|-)?([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?)|(([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?(p|P)(\+|-)?([0-9]|[A-F]|[a-f])((([0-9]|[A-F]|[a-f])|\_)*([0-9]|[A-F]|[a-f]))?))(d|D)?)'
