#!/usr/bin/env python

import sys
import argparse

#parses a string input
def parseInput(userInput):
	if userInput.startswith("(") and userInput.endswith(")"):
		#remove parens
		userInput = userInput[1: -1]

		#lambda
		if userInput.startswith("lambda") or userInput.startswith("λ"):
			return parseLambda(userInput)
		#print
		elif userInput.startswith("println"):
			return parsePrintln(userInput)
		#binop
		elif userInput.startswith("+") or userInput.startswith("*"):
			return parseBinOp(userInput)
		#ifleq
		elif userInput.startswith("ifleq0"):
			return parseIfleq0(userInput)
		#other expression
		else:
			return parseExpr(userInput)

	# is a number
	elif isNum(userInput):
		return userInput
	# is a symbol
	else:
		return userInput

# parses expressions of type (lambda (id) LC)
def parseLambda(userInput):
	parts = splitExpr(userInput, 3)
	if len(parts) != 3:
		formatError("lambda", userInput, "(lambda (id) LC)")

	if parts[1].startswith("(") and parts[1].endswith(")"):
		parts[1] = parts[1][1: -1]
	else:
		formatError("lambda", userInput, "(lambda (id) LC)")

	return "(lambda " + parts[1] + ": " + parseInput(parts[2]) + ")"

# parses expressions of type (println LC)
def parsePrintln(userInput):
	parts = splitExpr(userInput, 2)
	if len(parts) != 2:
		formatError("println", userInput, "(println LC)")

	return "specialPrint(" + parseInput(parts[1]).replace("\n", "\" +\n\"") + ")"

# parses expressions of type (+ LC LC) or (* LC LC)
def parseBinOp(userInput):
	parts = splitExpr(userInput, 3)
	if len(parts) != 3 and parts[0] != "+" and parts[0] != "*":
		formatError("binop", userInput, "(+ LC LC) or (* LC LC)")

	return ("(" + parseInput(parts[1]) + " " + parts[0] + 
		" " + parseInput(parts[2]) + ")")

# parses expressions of type (ifleq0 LC LC LC)
def parseIfleq0(userInput):
	parts = splitExpr(userInput, 4)
	if len(parts) != 4:
		formatError("ifleq0", userInput, "(ifleq0 LC LC LC)")

	return ("(" + parseInput(parts[2]) + " if " + parseInput(parts[1]) + 
		" <= 0 else " + parseInput(parts[3]) + ")")

# parses expressions of type (LC LC)
def parseExpr(userInput):
	parts = splitExpr(userInput, 2)
	if len(parts) != 2:
		formatError("expr", userInput, "(LC LC)")

	return parseInput(parts[0]) + " (" + parseInput(parts[1]) + ")"

# splits a string based on spaces but accounts for groups of parenthesis
# userInput - the string to split
# num - number of items that should be in the resulting list
def splitExpr(userInput, num):
	parts = []
	ndx = 0
	lastNdx = 0
	parensDeep = 0

	#goes until the specfied number of groups are found or the string is parsed
	while (num > 0 and ndx < len(userInput)):
		if userInput[ndx] == "(":
			parensDeep += 1
		elif userInput[ndx] == ")":
			parensDeep -= 1
		elif userInput[ndx] == " " and parensDeep == 0:
			num -= 1
			parts.append(userInput[lastNdx: ndx])
			lastNdx = ndx + 1
		ndx += 1

	if parensDeep == 0 and num > 0:
		parts.append(userInput[lastNdx: ndx])

	return parts

# prints an error with the given and expected values then exits
def formatError(expr, userInput, expected):
	print("Incorrect format for " + expr + "! GOT: " + 
		userInput + ", EXPECTED: " + expected)
	sys.exit(1)

# determines if the string is a number
def isNum(inputStr):
	try:
		float(inputStr)
		return True
	except ValueError:
		return False

# reads in the file input and removes whitespace
def getInput(inputFile):
	with open(inputFile, 'r') as f:
		content = f.read().replace("\n", "")
		return ' '.join(content.split())

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--infile', help='input file with lambda calculus')
	parser.add_argument('-o', '--outfile', default='result.py', help='output file')
	args = parser.parse_args()

	value = parseInput(getInput(args.infile))

	#add special print helper function if println was used
	#basically makes print return 0 instead of None
	if "specialPrint" in value:
		value = "def specialPrint(stuff):\n   print(stuff)\n   return 0\n\n" + value

	#write to a python file
	outputFile = args.outfile if args.outfile.endswith(".py") else args.outfile + ".py"
	with open(outputFile, "w") as f:
		f.write(value)
	f.close()

if __name__ == '__main__':
   main()