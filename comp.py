"""
Beej Computer Emulator

Software that pretends to be hardware

Turing Complete--it can solve any problem for which there is an algorithm.
"""

"""
Memory--like a big array

"Index into the memory array" == "address" == "pointer"
"""

import sys

#memory = [0] * 256  # RAM

PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3    # SAVE_REG R1,37   register[1] = 37
PRINT_REG = 4   # PRINT_REG R1     print(register[1])
ADD = 5

memory = [
	SAVE_REG, # SAVE_REG R1,37
	1,  # <-- index into the register array
	99, # <-- value that we want to store there
	SAVE_REG,
	2,  # <-- index into the register array
	11, # <-- value that we want to store there
	ADD, # ADD R1, R2  register[1] += register[2]
	1,
	2,
	PRINT_REG,
	1,
	PRINT_BEEJ,
	HALT,
]

register = [0] * 8 # 8 general-purpose registers, like variables, R0, R1, R2 .. R7

pc = 0  # Program Counter, index of the current instruction
running = True

while running:
	ir = memory[pc]  # Instruction register

	if ir == PRINT_BEEJ:
		print("Beej!")
		pc += 1

	elif ir == SAVE_REG:
		reg_num = memory[pc + 1]
		value = memory[pc + 2]
		register[reg_num] = value
		pc += 3

	elif ir == PRINT_REG:
		reg_num = memory[pc + 1]
		print(register[reg_num])
		pc += 2

	elif ir == ADD:
		reg_num1 = memory[pc + 1]
		reg_num2 = memory[pc + 2]
		register[reg_num1] += register[reg_num2]
		pc += 3

	elif ir == HALT:
		running = False
		pc += 1

	else:
		print(f'Unknown instruction {ir} at address {pc}')
		sys.exit(1)

