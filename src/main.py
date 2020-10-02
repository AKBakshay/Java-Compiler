#!/usr/bin/env python3

import argparse
import sys 
import os 

parser = argparse.ArgumentParser(description='tool to parse the Java 8 grammar.')

parser.add_argument('--input',type=str, default='./tests/input.java',help='Input file name')
parser.add_argument('--output',type=str, default='./tests/output.java',help='Output file name')
parser.add_argument('--verbose',type=str, default="False",help='Additional Information')

args = parser.parse_args()
args.input = "." + args.input 
os.chdir("./src")
os.system("python removeParanthesis.py {}".format(args.input))

os.system("java -cp .:antlr-4.8-complete.jar  org.antlr.v4.gui.TestRig Java8 compilationUnit -tree  ../tests/tmp.java > SDT.txt")
if args.verbose:
	os.system("python SDT2AST.py --output {} --verbose {}".format(args.output,args.verbose))
else:
	os.system("python SDT2AST.py --output {}".format(args.output))

out_name = args.output.split('.')[0]
os.system("dot -Tps {}.dot -o {}.ps".format(out_name,out_name))
os.system("mv {}.ps ../".format(out_name))
os.system("mv {}.dot ../".format(out_name))

