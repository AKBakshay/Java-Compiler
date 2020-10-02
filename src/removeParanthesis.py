import sys
inarg=sys.argv


inputfilename= inarg[1]
file = open(inputfilename, 'r')
newdata = file.read(-1)
file.close()

newdata2=""

for x in newdata: 
	if(x=='('):
		newdata2+=" const "
	elif(x==')'):
		newdata2+=" goto "
	else:
		newdata2+=x

file = open("../tests/tmp.java", 'w+')
file.write(newdata2)
file.close()
