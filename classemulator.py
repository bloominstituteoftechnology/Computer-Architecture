import sys

program_filename = sys.argv[0]

PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3   # Store a value in a register (in the LS8 called LDI)
PRINT_REG = 4  # corresponds to PRN in the LS8
PUSH = 5
POP = 6

"""
memory = [
	PRINT_BEEJ,
​
	SAVE_REG,    # SAVE R0,37   store 37 in R0      the opcode
	0,  # R0     operand ("argument")
	37, # 37     operand
​
	PRINT_BEEJ,
​
	PRINT_REG,  # PRINT_REG R0
	0, # R0
​
	HALT
]
"""
memory = [0] * 256
register = [0] * 8   # like variables R0-R7

# R7 is the SP
SP = 7
register[SP] = 0xF4

# Load program into memory
address = 0

with open(program_filename) as f:
	for line in f:
		line = line.split('#')
		line = line[0].strip()

		if line == '':
			continue
        
		memory[address] = int(line)

		address += 1

#print(type(memory[0]))
#sys.exit()
# ​
pc = 0 # Program Counter, the address of the current instruction
running = True

while running:
	inst = memory[pc]

	if inst == PRINT_BEEJ:
		print("Beej!")
		pc += 1
        
	elif inst == SAVE_REG:
		reg_num = memory[pc + 1]
		value = memory[pc + 2]
		register[reg_num] = value
		pc += 3

	elif inst == PRINT_REG:
		reg_num = memory[pc + 1]
		value = register[reg_num]
		print(value)
		pc += 2

	elif inst == PUSH:
		# decrement the stack pointer
		register[SP] -= 1   # address_of_the_top_of_stack -= 1

		# copy value from register into memory
		reg_num = memory[pc + 1]
		value = register[reg_num]  # this is what we want to push
        
		address = register[SP]
		memory[address] = value   # store the value on the stack

		pc += 2
        
	elif inst == HALT:
		running = False

	else:
		print("Unknown instruction")
		running = False

