# a simple virtual CPU
# a program that pretends to be a cpu

# to do:
# * store a sequence of instructions
# * go through these instructions, doing whatever they ask me to do

# Instructions
# * Print "Beej" on the screen
# * Halts the program

# grab value from each register, assign r0 to the value of them together
# the total of r0 and r1 is limited to 255
# in a 8-bi machine, 256+1 == 0 

import sys
​
PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3   # Save a value in a register
PRINT_REG = 4
ADD = 5   # Add two registers, r0 += r1
​
memory = [
	PRINT_BEEJ, # commands to execute
	SAVE_REG,  # SAVE_REG R0, 12 <-- PC
	0,
	37,
	SAVE_REG,
	1,
	12,
	ADD,
	0,
	1,
	PRINT_REG, # PRINT_REG R0
	0,
	PRINT_BEEJ,
	HALT
]
​
registers = [0,0,0,0,0,0,0,0]  # Like variables, named R0-R7 at disposal 
​
halted = False
​
pc = 0  # "Program Counter": index into the memory array,
        # AKA "pointer", "address", "location"
​
while not halted:
	instruction = memory[pc]
​
	if instruction == PRINT_BEEJ:
		print("Beej!")
		pc += 1
​
	elif instruction == SAVE_REG: # if we want to save something in register, we have to indicate what value where
		reg_num = memory[pc + 1] # next index in memory, can extract from memory
		value = memory[pc + 2]
​
		registers[reg_num] = value
​
		pc += 3
​
	elif instruction == PRINT_REG:
		reg_num = memory[pc + 1]
		print(registers[reg_num])
​
		pc += 2
​
	elif instruction == ADD:
		reg_num_a = memory[pc + 1]
		reg_num_b = memory[pc + 2]
​
		registers[reg_num_a] += registers[reg_num_b]
​
		pc += 3
​
​
	elif instruction == HALT:
		halted = True
​
	else:
		print(f'unknown instruction {instruction} at address {pc}')
		sys.exit(1)





# What are some good Operating System (OS) resources?
# To be clear, we're not talking about OSes this week, so all this is purely optional material. (In short, the OS is the software that controls your access to the hardware and peripherals.)
# OS from scratch tutorial: https://github.com/cfenollosa/os-tutorial
# OS01 free book: https://tuhdo.github.io/os01/
# Writing an OS in Rust: https://os.phil-opp.com/
# The Design of the UNIX Operating System by Maurice J. Bach (edited) 