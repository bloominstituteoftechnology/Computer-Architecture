"""CPU functionality."""

import sys

HLT = 0b00000001 # Hault
LDI = 0b10000010 # Load
PRN = 0b01000111 # Print
MUL = 0b10100010 # Multiply
PUSH = 0b01000101
POP = 0b01000110

class CPU:

	def __init__(self):
		self.running = True
		self.pointer = 0
		self.reg = [0] * 8
		self.memory = [0] * 256
		self.stackPointer = 0xf4
		self.reg[7] = self.stackPointer

		self.branchTable = {}
		self.branchTable[HLT] = self.handleHLT
		self.branchTable[LDI] = self.handleLDI
		self.branchTable[PRN] = self.handlePRN
		self.branchTable[MUL] = self.handleMUL
		self.branchTable[PUSH] = self.handlePUSH
		self.branchTable[POP] = self.handlePOP


	def load(self):
		file = sys.argv[1]

		try:
			with open(file) as data:
				for x, line in enumerate(data):
					line = line.split("#")
					v = int(line[0], 2)
					self.ram_write(x, v)

		except FileNotFoundError:
			print("Unable to open file")
			self.running = False


	def ram_read(self, value):
		return self.memory[value]


	def ram_write(self, value, data):
		self.memory[value] = data


	def handleHLT(self, a=None, b=None):
		self.running = False


	def handleLDI(self, a, b):
		self.reg[a] = b
		self.pointer +=3


	def handlePRN(self, a, b=None):
		print(self.reg[a])
		self.pointer += 2


	def handleMUL(self, a, b):
		self.alu("MUL", a, b)
		self.pointer += 3


	def handlePUSH(self, a, b=None):
		value = self.reg[a] # Get value from register
		self.stackPointer -= 1 # Decrement stackPointer
		self.memory[self.stackPointer] = value # Store to memory (RAM)
		self.pointer += 2


	def handlePOP(self, a, b=None):
		value = self.memory[self.stackPointer] # Get value from register
		self.reg[a] = value # Store to register
		self.stackPointer += 1
		self.pointer += 2


	def run(self):

		while self.running:
			instruction = self.ram_read(self.pointer)
			operand_a = self.ram_read(self.pointer + 1)
			operand_b = self.ram_read(self.pointer + 2)

			if instruction in self.branchTable:
				self.branchTable[instruction](operand_a, operand_b)
				self.trace()
			else:
				print("Error running program instructions")
				self.running = False


	def alu(self, op, a, b):

		if op == "ADD":
			self.reg[a] += self.reg[b]
		elif op == "SUB":
			self.reg[a] -= self.reg[b]
		elif op == "MUL":
			self.reg[a] * self.reg[b]
		elif op == "DIV":
			self.reg[a] // self.reg[b]
		elif op == "MOD":
			self.reg[a] % self.reg[b]

		else:
			raise Exception("Unsupported ALU operation")

	def trace(self):

		print(f"TRACE: %02X | %02X %02X %02X |" % (
			self.pointer,
			#self.fl,
			#self.ie,
			self.ram_read(self.pointer),
			self.ram_read(self.pointer + 1),
			self.ram_read(self.pointer + 2)
		), end='')

		for i in range(8):
			print(" %02X" % self.reg[i], end='')

		print()
