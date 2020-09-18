
CALL and RET
------------
Subroutines
    Functions, but you can't pass anything in
    And they can't return anything
def foo():
    print("foo 1")
    return
def bar():
    print("bar 1")
    foo()
    print("bar 2") # addr_2
    return
print("main 1")
bar()
print("main 2")  # addr_1 <-- PC
Stack: <- top
CALL:
    push return address on stack
    set pc to address of subroutine
RET:
    pop return addr off top of stack
    set the pc to the return address



    ##############################



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
CALL = 7
RET = 8
​
registers[SP] = 0xF4  # Init SP
​
def push_value(value):
	# Decrement SP
	registers[SP] -= 1
​
	# Copy the value to the SP address
	top_of_stack_addr = registers[SP]
	memory[top_of_stack_addr] = value
​
def pop_value():
	# Get the top of stack addr
	top_of_stack_addr = registers[SP]
​
	# Get the value at the top of the stack
	value = memory[top_of_stack_addr]
​
	# Increment the SP
	registers[SP] += 1
​
	return value
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
		# Get the reg num to push
		reg_num = memory[pc + 1]
​
		# Get the value to push
		value = registers[reg_num]
​
		push_value(value)
​
		#print(memory[0xea:0xf4])
​
		pc += 2
​
	elif ir == POP:
		# Get reg to pop into
		reg_num = memory[pc + 1]
​
		# Get the value at the top of the stack
		value = pop_value()
​
		# Store the value in the register
		registers[reg_num] = value
​
		pc += 2
​
	elif ir == CALL:
		# Compute the return addr
		return_addr = pc + 2
​
		# Push return addr on stack
		push_value(return_addr)
​
		# Get the value from the operand reg
		reg_num = memory[pc + 1]
		value = registers[reg_num]
​
		# Set the pc to that value
		pc = value
​
	#elif ir == RET:
		# TODO
​
​
	else:
		print(f"Unknown instruction {ir}")
		sys.exit(3)
​
	"""
	# For the LS-8 to move the PC
​
	# Any of these three lines should work
	inst_sets_pc = (ir >> 4) & 1 == 1
	inst_sets_pc = ir & 16 != 0
	inst_sets_pc = ir & 16  # Does this work?
​
	if not inst_sets_pc:  # if not CALL, RET, etc.
		number_of_operands = (ir & 0b11000000) >> 6
​
		how_far_to_move_pc = number_of_operands + 1
​
		pc += how_far_to_move_pc
	"""




    ############################

    3 # SAVE_REG R0,37
0
37
4 # PRINT_REG R0
0
​
3 # SAVE_REG R1,13
1
13
​
7 # CALL R1
1
7 # CALL R1
1
​
2 # HALT
​
# Subroutine:
1 # PRINT_BEEJ  # address 13
1 # PRINT_BEEJ
1 # PRINT_BEEJ
8 # RET