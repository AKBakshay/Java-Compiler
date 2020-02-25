import sys
import re
import ply.lex as lex
import csv
from regex import *
from collections import defaultdict as ddict

filename = sys.argv[1]
outfilename = sys.argv[2]
input_data = open(filename,'r').read()

#initialize lexer

lexer=lex.lex()
lexer.input(input_data)

Keyword = ddict(int)
Identifier = ddict(int)
Separator = ddict(int) 
Operator = ddict(int)
Literal = ddict(int)

for tok in lexer:
	#print(str(tok.lineno)+' '+str(tok.type)+'   '+str(tok.value))
	if(tok.type == "COMMENT"):
		continue

	if(tok.type in separators):
		Separator[tok.value] += 1

	elif(tok.type in list(reserved.values())):
		if(tok.type == 'NULLVAL' or tok.type == 'TRUEVAL' or tok.type == 'FALSEVAL'):
			Literal[tok.value] +=1
		else:
			Keyword[tok.value] += 1

	elif(tok.type in operators):
		Operator[tok.value] += 1

	elif(tok.type in types):
		Literal[tok.value] += 1

	elif(tok.type in identity):
		Identifier[tok.value] += 1
	else :
		print("Impossible State!")

with open(outfilename,'w',newline = '') as myFile:
	writer = csv.writer(myFile)
	field_names = ['Lexeme','Token','Count']
	writer.writerow(field_names)
	for x in Identifier:
		writer.writerow([str(x),'Identifier',Identifier[x]])
	for x in Keyword:
		writer.writerow([str(x),'Keyword',Keyword[x]])
	for x in Separator:
		writer.writerow([str(x),'Separator',Separator[x]])
	for x in Operator:
		writer.writerow([str(x),'Operator',Operator[x]])
	for x in Literal:
		writer.writerow([str(x),'Literal',Literal[x]])

print("We are now done!")
