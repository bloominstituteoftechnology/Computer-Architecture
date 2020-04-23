#!/usr/bin/env python

"""CPU functionality."""

import re
import sys

from datetime import datetime


class CPU:
	"""Main CPU class."""

	def __init__(self, debug=False):
		"""Construct a new self."""
		self.debug = debug
		self.registers = [0b00000000] * 8
		self.registers[7] = 0xF4
		self.pc = 0b00000000  # Program Counter
		# self.ir = 0b00000000  # Instruction Register
		# self.mar = 0b00000000  # Memory Address Register
		# self.mdr = 0b00000000  # Memory Data Register
		self.fl = 0b11000000  # Flags Register
		# RI000LGE
		# Running, Interrupts Enabled, Less than, Greater than, Equal

		self.ram = [0b00000001] * 0b11111111

		self._last_second = datetime.now()

		from operations import ops
		self.ops = ops

	# Interrupt Mask is R5
	@property
	def IM(self):
		return self.registers[5]

	@IM.setter
	def IM(self, value):
		self.registers[5] = value

	# Interrupt Status is R6
	@property
	def IS(self):
		return self.registers[6]

	@IS.setter
	def IS(self, value):
		self.registers[6] = value

	# Stack Pointer is R7
	@property
	def SP(self):
		return self.registers[7]

	@SP.setter
	def SP(self, value):
		self.registers[7] = value

	# Key Pressed is RAM: 0xF4
	@property
	def key_pressed(self):
		return self.ram_read(0xF4)

	@key_pressed.setter
	def key_pressed(self, value):
		self.ram_write(0xF4, value)

	def ram_read(self, mar):
		return self.ram[mar]

	def ram_write(self, mar, mdr):
		self.ram[mar] = mdr

	def load(self):
		"""Load a program into memory."""

		filename = sys.argv[1]
		with open(filename, 'r') as f:
			lines = f.read()
		cleaned_lines = re.findall(r'^[01]+', lines, flags=re.MULTILINE)
		program = [int(line, 2) for line in cleaned_lines]

		address = 0

		if self.debug:
			print('Loading program:')
		for instruction in program:
			if self.debug:
				print(f'{address:03}: {instruction:08b}')
			self.ram[address] = instruction
			address += 1

	def alu(self, op, reg_a, reg_b):
		"""ALU operations."""

		if op == "ADD":
			self.registers[reg_a] = self.registers[reg_a] + self.registers[reg_b] & 0xFF
		elif op == "MUL":
			self.registers[reg_a] = self.registers[reg_a] * self.registers[reg_b] & 0xFF
		elif op == "SUB":
			self.registers[reg_a] = self.registers[reg_a] - self.registers[reg_b] & 0xFF
		elif op == "XOR":
			self.registers[reg_a] = self.registers[reg_a] ^ self.registers[reg_b]
		elif op == "AND":
			self.registers[reg_a] = self.registers[reg_a] & self.registers[reg_b]
		elif op == "OR":
			self.registers[reg_a] = self.registers[reg_a] | self.registers[reg_b]
		elif op == "SHR":
			self.registers[reg_a] = self.registers[reg_a] >> self.registers[reg_b]
		elif op == "SHL":
			self.registers[reg_a] = self.registers[reg_a] << self.registers[reg_b] & 0xFF
		elif op == "CMP":
			# Clear the LGE flags
			self.fl = self.fl & 0b11111000
			# Set the appropriate flags by comparison
			if self.registers[reg_a] == self.registers[reg_b]:
				self.fl = self.fl | 0b00000001
			elif self.registers[reg_a] > self.registers[reg_b]:
				self.fl = self.fl | 0b00000010
			elif self.registers[reg_a] < self.registers[reg_b]:
				self.fl = self.fl | 0b00000100
		elif op == "DEC":
			self.registers[reg_a] = self.registers[reg_a] - 1 & 0xFF
		elif op == "INC":
			self.registers[reg_a] = self.registers[reg_a] + 1 & 0xFF
		elif op == "NOT":
			self.registers[reg_a] = self.registers[reg_a] ^ 0xFF
		elif op == "DIV":
			if self.registers[reg_b] == 0:
				raise Exception("Division by zero")
			self.registers[reg_a] = self.registers[reg_a] // self.registers[reg_b]
		elif op == "MOD":
			if self.registers[reg_b] == 0:
				raise Exception("Division by zero")
			self.registers[reg_a] = self.registers[reg_a] % self.registers[reg_b]
		else:
			raise Exception("Unsupported ALU operation")

	def trace(self):
		"""
		Handy function to print out the CPU state. You might want to call this
		from run() if you need help debugging.
		"""

		print(f"TRACE: %s | %s %s %s |" % (
			format(self.pc, '08b'),
			#self.fl,
			#self.ie,
			format(self.ram_read(self.pc), '08b'),
			format(self.ram_read(self.pc + 1), '08b'),
			format(self.ram_read(self.pc + 2), '08b')
		), end='')

		for i in range(8):
			print(" %s" % format(self.registers[i], '08b'), end='')

		print()

	def _check_timer_interrupt(self):
		# If timer interrupts are enabled
		if self.IM & 0b00000001:
			now = datetime.now()
			if (now - self._last_second).seconds >= 1:
				self._last_second = now
				self.IS = self.IS | 0b00000001

	def _check_keyboard_interrupt(self):
		# If keyboard interrupts are enabled
		if self.IM & 0b00000010:
			try:
				c = sys.stdin.read(1)
				if c:
					self.IS = self.IS | 0b00000010
					self.key_pressed = ord(c) & 0xFF
			except IOError:
				pass

	def _handle_interrupts(self):
		# Check for interrupts
		self._check_timer_interrupt()
		self._check_keyboard_interrupt()

		maskedInterrupts = self.IM & self.IS
		if self.debug and maskedInterrupts:
			print(f'Interrupt caught, maskedInterrupts: {maskedInterrupts:08b}')
			print(f'Interrupt Mask: {self.IM:08b}, Interrupt Status: {self.IS:08b}')
		for i in range(8):
			# If bit i in the IS register is set
			if ((maskedInterrupts >> i) & 1) == 1:
				if self.debug:
					print(f'Interrupt found at bit {i}')
				# Disable further interrupts
				self.fl = self.fl & 0b10111111
				# Clear the bit in the IS register
				self.IS = self.IS & ((1 << i) ^ 0xFF)
				# Push the PC register
				self.SP -= 1
				self.ram_write(self.SP, self.pc)
				# Push the FL register
				self.SP -= 1
				self.ram_write(self.SP, self.fl)
				# Push R0-R6, in that order
				for r in range(7):
					self.ops[0b01000101](self, r)
				# Look up the vector from the interrupt vector table
				vector = self.ram_read(0xF8 + i)
				self.pc = vector
				break

	def run(self):
		"""Run the self."""

		# As long as our running flag is set
		while self.fl & 0b10000000:

			# If interrupts are enabled
			if self.fl & 0b01000000:
				self._handle_interrupts()

			ir = self.ram_read(self.pc)  # Load the instruction
			if self.debug:
				print(f'Reading instruction at address {self.pc:08b} ({self.pc:03}): {ir:08b}')

			# Load as many operands as the top two bits call for
			operand_1 = 0b00000000
			operand_2 = 0b00000000
			if ir & 0b11000000:
				operand_1 = self.ram_read(self.pc + 1)
			if ir & 0b10000000:
				operand_2 = self.ram_read(self.pc + 2)

			try:
				if self.debug:
					print(f'Instruction {self.ops[ir].__name__} called with operands {operand_1:08b}, {operand_2:08b}')
				# Call the operation based on the lower four bits
				self.ops[ir](self, operand_1, operand_2)
			except (Exception, KeyboardInterrupt):
				self.trace()
				raise

			# If the fourth bit is *not* set, increment the PC
			# If the fourth bit *is* set, the operation sets the PC
			if not ir & 0b00010000:
				# Increment the PC by 1 + the left two bits
				self.pc += ((ir & 0b11000000) >> 6) + 1
