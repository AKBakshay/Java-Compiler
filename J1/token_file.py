#This file contains the full token list for Java 8.0

#tokens initially contains: SEPARATORS and COMMENT
separators = [
	'LPAR',
	'RPAR',
	'LCURL',
	'RCURL',
	'LSQR',
	'RSQR',
	'SCOLON',
	'COMMA',
	'POINT',
	'VARARGS',
	'ATRATE',
	'MTREF'
	]

comment = [
	'COMMENT'
	]

#includes false, true, null also
reserved = {
	'abstract' : 'ABSTRACT',
	'continue' : 'CONTINUE',
	'for' : 'FOR',
	'new' : 'NEW',
	'switch' : 'SWITCH',
	'assert' : 'ASSERT',
	'default' : 'DEFAULT',
	'if' : 'IF',
	'package' : 'PACKAGE',
	'synchronized' : 'SYNCHRONIZED',
	'boolean' : 'BOOLEAN',
	'do' : 'DO',
	'goto' : 'GOTO',
	'private' : 'PRIVATE',
	'this' : 'THIS',
	'break' : 'BREAK',
	'double' : 'DOUBLE',
	'implements' : 'IMPLEMENTS',
	'protected' : 'PROTECTED',
	'throw' : 'THROW',
	'byte' : 'BYTE',
	'else' : 'ELSE',
	'import' : 'IMPORT',
	'public' : 'PUBLIC',
	'throws' : 'THROWS',
	'case' : 'CASE',
	'enum' : 'ENUM',
	'instanceof' : 'INSTANCEOF',
	'return' : 'RETURN',
	'transient' : 'TRANSIENT',
	'catch' : 'CATCH',
	'extends' : 'EXTENDS',
	'int' : 'INT',
	'short' : 'SHORT',
	'try' : 'TRY',
	'char' : 'CHAR',
	'final' : 'FINAL',
	'interface' : 'INTERFACE',
	'static' : 'STATIC',
	'void' : 'VOID',
	'class' : 'CLASS',
	'finally' : 'FINALLY',
	'long' : 'LONG',
	'strictfp' : 'STRICTFP',
	'volatile' : 'VOLATILE',
	'const' : 'CONST',
	'float' : 'FLOAT',
	'native' : 'NATIVE',
	'super' : 'SUPER',
	'while' : 'WHILE',
	'null' : 'NULLVAL',
	'false' : 'FALSEVAL',
	'true' : 'TRUEVAL'
	}

operators = [
	'EQ',
	'GRTHAN',
	'LETHAN',
	'EXCLAIM',
	'TILDE',
	'QMARK',
	'COLON',
	'ARROW',
	'DEQ',
	'GREQ',
	'LEEQ',
	'NTEQ',
	'DAND',
	'DOR',
	'DPLUS',
	'DMINUS',
	'PLUS',
	'MINUS',
	'STAR',
	'FSLASH',
	'AND',
	'OR',
	'XOR',
	'MOD',
	'LSHIFT',
	'RSHIFT',
	'URSHIFT',
	'PLUSEQ',
	'MINUSEQ',
	'STAREQ',
	'FSLASHEQ',
	'ANDEQ',
	'OREQ',
	'XOREQ',
	'MODEQ',
	'LSHIFTEQ',
	'RSHIFTEQ',
	'URSHIFTEQ'
	]
# boolean values are covered in reserved
# null value is covered in reserved

types = [
	'INTVAL',
	'LONGVAL',
	'FLOATVAL',
	'CHARVAL',
	'DOUBLEVAL',
	'STRINGVAL',
	]

identity = [
	'IDENTIFIER'
	]

tokens = separators + comment + list(reserved.values()) + operators + identity + types
#print(tokens)

