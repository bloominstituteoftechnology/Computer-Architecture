# The index into the memory array, AKA location, address, pointer
# 1 - PRINT_BEEJ
# 2 - HALT
# 3 - SAVE_REG  store a value in a register
# 4 - PRINT_REG  print the register value in decimal

memory = [   # think of as a big array of bytes, 8-bits per byte
	1,  # PRINT_BEEJ

	3,  # SAVE_REG R4 37, instruction itself also called "opcode"
	4,  # 4 and 37 are arguments to SAVE_REG, also called "operands"
	37,

	4,  # PRINT_REG R4
	4,

	2   # HALT
]

registers = [0] * 8

running = True

pc = 0   # Program Counter, the index into memory of the currently-executing instruction

while running:
	ir = memory[pc]  # Instruction Register

	if ir == 1:  # PRINT_BEEJ
		print("Beej!")
		pc += 1

	elif ir == 2:  # HALT
		running = False
		pc += 1

	elif ir == 3:  # SAVE_REG
		reg_num = memory[pc + 1]
		value = memory[pc + 2]
		registers[reg_num] = value

		pc += 3
  
	elif ir == 4:  # PRINT_REG
		reg_num = memory[pc + 1]
		print(registers[reg_num])

		pc += 2