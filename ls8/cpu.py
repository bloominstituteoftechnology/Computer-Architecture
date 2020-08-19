"""CPU functionality."""

import sys

class CPU:

	def __init__(self):
		self.running = True
		self.pointer = 0
		self.reg = [0] * 8
		self.memory = [0] * 256


	def load(self):

		file = sys.argv[1]
		try:
			with open(file) as data:
				for x, line in enumerate(data):
					line = line.split("#")
					#print("line ~",line)

					try:
						v = int(line[0], 2) 
					except ValueError:
						continue

					self.memory[x] = v

		except FileNotFoundError:
			print("Unable to open file")
			self.running = False


	def alu(self, op, reg_a, reg_b):
		"""ALU operations."""

		if op == "ADD":
			self.reg[reg_a] += self.reg[reg_b]
		elif op == "SUB":
			self.reg[reg_a] += -self.reg[reg_b]
		elif op == "MUL":
			product = self.reg[reg_a] * self.reg[reg_b]
			self.reg[reg_a] = product
		else:
			raise Exception("Unsupported ALU operation")

	def trace(self):
		"""
		Handy function to print out the CPU state. You might want to call this
		from run() if you need help debugging.
		"""

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

	def ram_read(self, value):
		return self.memory[value]

	def ram_write(self, value, data):
		self.memory[value] = data

	def run(self):

		HLT = 0b00000001 # Hault
		LDI = 0b10000010 # Load
		PRN = 0b01000111 # Print
		MUL = 0b10100010 # Multiply

		while self.running:
			instruction = self.ram_read(self.pointer)
			operand_a = self.ram_read(self.pointer + 1)
			operand_b = self.ram_read(self.pointer + 2)

			if instruction is HLT: # Hault
				self.running = False
				self.pointer += 1

			if instruction is LDI: # Load
				self.reg[operand_a] = operand_b
				self.pointer += 3

			if instruction is PRN: # Print
				operand_a = self.ram_read(self.pointer + 1)
				print(self.reg[operand_a])
				self.pointer += 2

			if instruction == MUL: # Multiply
				multiply = self.reg[operand_a] * self.reg[operand_b]
				print(multiply)
				self.pointer += 3



