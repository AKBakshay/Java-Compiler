import ply.lex as lex 
import pdb
import sys
import lex_tokeniser 
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--output',type=str, default='output.java',help='Output file name')
parser.add_argument('--verbose',type=str, default="False",help='Additional Information')

args = parser.parse_args()

f = open("SDT.txt",'r')
data = f.read(-1)
f.close()

tokens = (
            'EOF',
            'data',
            'lbrace',
            'rbrace',
            'comma' ,
            'ignore',
            'String',
            'Operator',
            'cbrace',
            'sqbrace',
            'RMsymbols',
            'GOTO',
            'CONST'
        )

# t_EOF = r'<EOF>'
t_comma = r','
t_lbrace = r'\('
t_rbrace = r'\)'
t_ignore  = ' \t\f\n'
t_cbrace = r'\{|\}'
t_sqbrace = r'\[|\]'


def t_GOTO(t):
    r'\bgoto\b'
    return t 

def t_CONST(t):
    r'\bconst\b'
    return t 

def t_EOF(t):
    r'<EOF>'
    return t

def t_data(t):
    r'[0-9a-zA-Z_]+'
    return t

def t_Operator(t):
    r'>>>=|>>=|<<=|\+=|-=|\*=|/=|&=|\|=|\^=|%=|<<|->|==|>=|<=|!=|&&|\|\||\+\+|--|=|>|<|!|~|\?|:|\+|-|\*|/|&|\||\^|%'
    return t

def t_String(t):
     r'"(\\[0-3]?[0-7]?[0-7]|[^\r\n"\\]?(\\b)?(\\t)?(\\n)?(\\f)?(\\r)?(\\")?(\\\')?(\\\\)?)*"|\'(\\[0-3]?[0-7]?[0-7]|[^\r\n\t\f"\'\\]|(\\b)|(\\t)|(\\n)|(\\f)|(\\r)|(\\")|(\\\')|(\\\\))\''
     return t

def t_RMsymbols(t):
    r'\W'
    return t


def t_error(t):
    print("Illegal character '{}' in line {}".format(t.value[0], t.lexer.lineno))
    print("Lexical Analysis Terminating")
    sys.exit()


def func(lexer):
    # Parse the string output from AntLR
    result = []

    tok = lexer.token()
    while tok.value != ')':
        if tok.value == '(' :
            result.append(func(lexer))
        else:
            result.append(tok.value)
        tok = lexer.token()
    return result
    
def SDT2AST(x):
    # Removing intermediate long chain of nodes
    y = []
    if type(x) is list:
        if len(x) == 2:
            return SDT2AST(x[1])
        else:
            for l in range(1,len(x)):
                x[l] = SDT2AST(x[l])
            
            return x
    else:
        return x


def numbering(x):
    # numbering all the tokens in x for converting to .dot file
    result = []
    global count

    for l in x:
        if type(l) is list:
            result.append(numbering(l))
        else:
            result.append(count)
            if l=='goto':
                id_mapping[count] = ')'
            elif l=='const':
                id_mapping[count] = '('
            else:
                id_mapping[count] = l
            leaf_node[count] = True
            count += 1
            
    return result


def getDOT(x,leaf_node,f):
    for i in range(1,len(x)):
        if type(x[i]) is list:
            f.write("{} -> {}\n".format(x[0],x[i][0]))
            getDOT(x[i],leaf_node,f)    
        else:
            f.write("{} -> {}\n".format(x[0],x[i]))
        leaf_node[x[0]] = False 
            



def upShifting(x):
    # shifting the symbols to the parent nodes (when required)
    result = []
    for y in x:
        if type(y) is list:
            result.append(upShifting(y))
        else:
            if y in up_shifting_symbols:
                result[0] = y 
            else:
                result.append(y) 
    return result


up_shifting_symbols = [">>>=",">>=","<<=","+=","-=","*=","/=","&=","|=","^=","%=","<<","->","==",">=","<=","!=","&&","||","=",">","<","+","-","*","/", "&","|","^","%"]
add_quotes = ['Literal','Separator','Operator','String','EOF']

count = 0
id_mapping = {}
leaf_node = {}

# Parsing the string output from the AntLR

lexer = lex.lex()
lexer.input(data)

tok = lexer.token()

output = func(lexer)
output = SDT2AST(output)
up_bring = upShifting(output)
tmp_representation = numbering(up_bring)

if args.verbose=="True":
    print(tmp_representation)
    print(id_mapping)

f = open(args.output,'w')

f.write("digraph{\n")
getDOT(tmp_representation,leaf_node,f)

lexer = lex.lex(module=lex_tokeniser)

for (key,val) in id_mapping.items():
    lexer.input(val)
    tok = lexer.token()    
    if leaf_node[key]:
        if tok.type in add_quotes:
            if tok.type == 'String':
                f.write('{} [ label= "{}" ]\n'.format(key,str(tok.type)+"__" + tok.value.replace('"',"")))
            else:
                f.write('{} [ label= "{}__{}" ]\n'.format(key,tok.type,tok.value))
        else:
            f.write('{} [ label= {}__{} ]\n'.format(key,tok.type,tok.value))
    else:
        if tok.type in add_quotes:
            f.write('{} [ label= "{}" ]\n'.format(key,val))
        else:
            f.write('{} [ label= {} ]\n'.format(key,val))

f.write("}")
f.close()
