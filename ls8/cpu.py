#!/usr/bin/env python

"""CPU functionality."""

import re
import sys


class CPU:
	"""Main CPU class."""

	def __init__(self):
		"""Construct a new CPU."""
		self.registers = [0b00000000] * 8
		self.registers[7] = 0xF4
		self.pc = 0b00000000  # Program Counter
		# self.ir = 0b00000000  # Instruction Register
		# self.mar = 0b00000000  # Memory Address Register
		# self.mdr = 0b00000000  # Memory Data Register
		self.fl = 0b10000000  # Flags Register
		# First bit is used as `running` flag

		self.ram = [0b00000001] * 0b11111111

		from operations import ops
		self.ops = ops

	def ram_read(self, mar):
		return self.ram[mar]

	def ram_write(self, mar, mdr):
		self.ram[mar] = mdr

	def load(self, debug=False):
		"""Load a program into memory."""

		filename = sys.argv[1]
		with open(filename, 'r') as f:
			lines = f.read()
		cleaned_lines = re.findall(r'^[01]+', lines, flags=re.MULTILINE)
		program = [int(line, 2) for line in cleaned_lines]

		address = 0

		if debug:
			print('Loading program:')
		for instruction in program:
			if debug:
				print(f'{address:03}: {instruction:08b}')
			self.ram[address] = instruction
			address += 1

	def alu(self, op, reg_a, reg_b):
		"""ALU operations."""

		if op == "ADD":
			self.registers[reg_a] += self.registers[reg_b]
		elif op == "MUL":
			self.registers[reg_a] = self.registers[reg_a] * self.registers[reg_b]
		# elif op == "SUB": etc
		else:
			raise Exception("Unsupported ALU operation")

	def trace(self):
		"""
		Handy function to print out the CPU state. You might want to call this
		from run() if you need help debugging.
		"""

		print(f"TRACE: %02X | %02X %02X %02X |" % (
			self.pc,
			#self.fl,
			#self.ie,
			self.ram_read(self.pc),
			self.ram_read(self.pc + 1),
			self.ram_read(self.pc + 2)
		), end='')

		for i in range(8):
			print(" %02X" % self.registers[i], end='')

		print()

	def run(self, debug=False):
		"""Run the CPU."""

		# As long as our running flag is set
		while self.fl & 0b10000000:
			ir = self.ram_read(self.pc)  # Load the instruction
			if debug:
				print(f'Reading instruction at address {self.pc:08b}: {ir:08b}')

			# Load as many operands as the top two bits call for
			operand_1 = None
			operand_2 = None
			if ir & 0b11000000:
				operand_1 = self.ram_read(self.pc + 1)
			if ir & 0b10000000:
				operand_2 = self.ram_read(self.pc + 2)

			try:
				# Call the operation based on the lower four bits
				self.ops[ir](self, operand_1, operand_2)
			except Exception:
				self.trace()
				raise

			# If the fourth bit is *not* set, increment the PC
			# If the fourth bit *is* set, the operation sets the PC
			if not ir & 0b00010000:
				# Increment the PC by 1 + the left two bits
				self.pc += ((ir & 0b11000000) >> 6) + 1
