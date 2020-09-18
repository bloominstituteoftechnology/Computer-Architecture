import sys
​
"""
Get the file path from the command line
Sanitize the data from that file
	Ignore blank lines, whitespace, comments
	Splitting the input file per line
	Turn into program instructions (str->int)
"""
# These all mean the same thing:
#   Index into the memory array
#   Address
#   Location
#   Pointer
​
memory = [0] * 256  # RAM
​
registers = [0] * 8  # R0-R7
​
if len(sys.argv) != 2:
	print("usage: comp.py filename")
	sys.exit(1)
​
try:
	address = 0
​
	with open(sys.argv[1]) as f:
		for line in f:
			t = line.split('#')
			n = t[0].strip()
​
			if n == '':
				continue
​
			try:
				n = int(n)
			except ValueError:
				print(f"Invalid number '{n}'")
				sys.exit(1)
​
			memory[address] = n
			address += 1
​
except FileNotFoundError:
	print(f"File not found: {sys.argv[1]}")
	sys.exit(2)
​
# "Variables" in hardware. Known as "registers".
# There are a fixed number of registers
# They have fixed names
#  R0, R1, R2, ... , R6, R7
​
pc = 0  # Program Counter, address of the currently-executing instuction
​
SP = 7
​
PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3
PRINT_REG = 4
PUSH = 5
POP = 6
​
registers[SP] = 0xF4  # Init SP
​
running = True
​
while running:
	ir = memory[pc]  # Instruction Register, copy of the currently-executing instruction
​
	if ir == PRINT_BEEJ:
		print("Beej!")
		pc += 1
​
	elif ir == HALT:
		running = False
​
	elif ir == SAVE_REG: # (LDI on the LS8)
		reg_num = memory[pc + 1]
		value = memory[pc + 2]
		registers[reg_num] = value
		pc += 3
​
	elif ir == PRINT_REG:
		reg_num = memory[pc + 1]
		print(registers[reg_num])
		pc += 2
​
	elif ir == PUSH:
		# Decrement SP
		registers[SP] -= 1
​
		# Get the reg num to push
		reg_num = memory[pc + 1]
​
		# Get the value to push
		value = registers[reg_num]
​
		# Copy the value to the SP address
		top_of_stack_addr = registers[SP]
		memory[top_of_stack_addr] = value
​
		#print(memory[0xea:0xf4])
​
		pc += 2
​
	elif ir == POP:
		# Get reg to pop into
		reg_num = memory[pc + 1]
​
		# Get the top of stack addr
		top_of_stack_addr = registers[SP]
​
		# Get the value at the top of the stack
		value = memory[top_of_stack_addr]
​
		# Store the value in the register
		registers[reg_num] = value
​
		# Increment the SP
		registers[SP] += 1
​
		pc += 2
​
	else:
		print(f"Unknown instruction {ir}")
		sys.exit(3)
​
	"""
	# For the LS-8 to move the PC
​
	number_of_operands = (ir & 0b11000000) >> 6
​
	how_far_to_move_pc = number_of_operands + 1
​
	pc += how_far_to_move_pc
	"""





    ################################################
    3 # SAVE_REG R0,11
0
11
3 # SAVE_REG R1,22
1
22
5 # PUSH R0
0
5 # PUSH R1
1
6 # POP R0
0
6 # POP R1
1
4 # PRINT_REG R0  # 22
0
2 # HALT

#################################