# These all mean the same thing:
#   Index into the memory array
#   Address
#   Location
#   Pointer
​
memory = [
	1,  # PRINT_BEEJ  Address 0
	3,  # SAVE_REG R1,37
	1,
	37,
	4,  # PRINT_REG R1
	1,
	2,  # HALT
]
​
registers = [0] * 8  # R0-R7
​
# "Variables" in hardware. Known as "registers".
# There are a fixed number of registers
# They have fixed names
#  R0, R1, R2, ... , R6, R7
​
pc = 0  # Program Counter, address of the currently-executing instuction
​
running = True
​
while running:
	ir = memory[pc]  # Instruction Register, copy of the currently-executing instruction
​
	if ir == 1:  # PRINT_BEEJ
		print("Beej!")
		pc += 1
​
	elif ir == 2:
		running = False
​
	elif ir == 3:  # SAVE_REG
		reg_num = memory[pc + 1]
		value = memory[pc + 2]
		registers[reg_num] = value
		pc += 3
​
	elif ir == 4:  # PRINT_REG
		reg_num = memory[pc + 1]
		print(registers[reg_num])
		pc += 2
​
	else:
		print(f"Unknown instruction {b}")