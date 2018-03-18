import time
import os
import sys

LEFT = -1
RIGHT = 1
class TuringMachine:

	def __init__(self):
		self.tape = " "
		self.position = 0
		self.currentState = None
		self.states = {}

	def addState(self, name):
		self.states[name] = State(name)

	def addInstruction(self, stateName, readSymbol, writeSymbol, moveDirection, newStateName):
		if newStateName == "accept":
			self.states[stateName].addInstruction(readSymbol, writeSymbol, moveDirection, newStateName)
		else:
			self.states[stateName].addInstruction(readSymbol, writeSymbol, moveDirection, self.states[newStateName])

	def setConfiguration(self, tape, position, stateName):
		self.tape = tape
		self.position = position
		self.currentState = self.states[stateName]

	def readNextSymbol(self):
		action = self.currentState.readSymbol(self.tape[self.position])
		if action == "reject":
			self.currentState = "reject"
		else:
			self.tape = self.tape[:self.position] + action[0] + self.tape[self.position + 1:]
			self.position += action[1]
			if self.position == -1:
				self.tape = " " + self.tape
				self.position += 1
			elif self.position == len(self.tape):
				self.tape += " "
			self.currentState = action[2]

	def run(self, trace = False):
		os.system("cls")
		print("Initial tape: '" + self.tape + "'")
		while self.currentState != "accept" and self.currentState != "reject":
			self.readNextSymbol()
			if trace:
				sys.stdout.write("\r" + self.tape[:self.position])
				sys.stdout.flush()
				sys.stdout.write("\033[47m" + self.tape[self.position])
				sys.stdout.flush()
				sys.stdout.write("\033[0m" + self.tape[self.position + 1:])
				sys.stdout.flush()
				time.sleep(0.05)

		print("\nFinal tape: '" + self.tape.strip() + "'")
		print("Final State:", self.currentState)


class State:
	
	def __init__(self, name):
		self.instructions = {}
		self.name = name

	def addInstruction(self, readSymbol, writeSymbol, moveDirection, newState):
		self.instructions[readSymbol] = [writeSymbol, moveDirection, newState]

	def readSymbol(self, symbol):
		if symbol in list(self.instructions.keys()):
			return self.instructions[symbol]
		return "reject"

class TuringScript:

	def __init__(self, filepath):
		with open(filepath,"r") as readFile:
			self.source = readFile.read()
			self.states = {}
			self.configuration = [" ", 0, None]
			self.controlChars = ' ":,}{*'

	def parseCode(self):
		code = "".join(self.source.split("\n"))
		scope = 0
		varName = ""
		currentState = None
		instruction = []
		i = 0
		while i < len(code):
			char = code[i]
			if char == "{":
				scope += 1
			elif char == "}":
				scope -= 1 
			elif scope == 0:
				if char == "*":
					self.configuration[2] = currentState
				elif char == '"':
					self.configuration[0] = code[i+1:].split('"')[0]
					i += len(self.configuration[0]) + 1
				elif char in "1234567890" and len(varName) == 0:
					x = 0
					while i+x < len(code) and code[i+x] in "1234567890":
						x+=1
					self.configuration[1] = int(code[i:i+x])
					i+=x
				elif char != " ":
					varName += char
					if code[i+1] in self.controlChars:
						self.states[varName] = {}
						currentState = varName
						varName = ""

			else:
				if char == '"':
						instruction.append(code[i+1])
						i += 2
				elif char not in self.controlChars:
					if len(instruction) == 2:
						instruction.append(char)
					else:
						print(varName)
						varName += char
						if code[i+1] in self.controlChars:
							if instruction[2].lower() == "r":
								instruction[2] = 1
							else:
								instruction[2] = -1

							self.states[currentState][instruction[0]] = instruction[1:] + [varName]
							varName = ""
							instruction = []
			i += 1

	def createTuringMachine(self):
		tm = TuringMachine()
		for state in self.states.keys():
			tm.addState(state)
		for state in self.states.keys():
			for readChar in self.states[state].keys():
				instruction = self.states[state][readChar]
				tm.addInstruction(state, readChar, instruction[0], instruction[1], instruction[2])
		if self.configuration[2] == None:
			self.configuration[2] = self.states.keys[0]
		tm.setConfiguration(self.configuration[0], self.configuration[1], self.configuration[2])
		return tm

def runScript(filepath, trace = False):
	ts = TuringScript(filepath)
	ts.parseCode()
	tm = ts.createTuringMachine()
	tm.run(trace = trace)

def main():
	trace = False
	for item in sys.argv[2:]:
		if item == "-t":
			print("a")
			trace = True
	runScript(sys.argv[1], trace = trace)


main()