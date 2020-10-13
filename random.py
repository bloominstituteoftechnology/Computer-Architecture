import sys

# Memory holds bytes
# Big array of bytes
# To get data or set data in memory, you need the index in the array
# These terms are equivalent:
#Index, address, location, pointer

PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3
PRINT_REG = 4

memory = [
	1,   # PRINT_BEEJ
    3,   # SAVE_REG R1,37    r[1] = 37
	1,   # R1
	37,
	4,   # PRINT_REG R1      print(r[1])
	1,   # R1
	1,   # PRINT_BEEJ
	2    # HALT
]

register = [0] * 8 #[0, 0, 0, 0, 0, 0, 0, 0]

# Variables are called registers
# There are a fixed number of them
# They have preset names

# Start execution at address 0

# Keep track of the address of the currently-executing instruction

pc = 0  # program counter, pointer to the instruction we're executing

halted = False


while not halted:
    instruction = memory[pc]
    if instruction == PRINT_BEEJ:
        print("Beej!")
        pc += 1
    elif instruction == HALT:
        halted = True
        pc += 1

    elif instruction == SAVE_REG:
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        register[reg_num] = value

        pc += 3
    elif instruction == PRINT_REG:
        reg_num = memory[pc + 1]
        print(register[reg_num])
        pc += 2
    else:
        print(f"unknown instruction {instruction} at address {pc}")
        sys.exit(1)


# print(0xFF)
# print(bin(0x87))

#1 + 2 + 4 + 0 + 0 + 0 + 0 + 128
#1 + 2 + 4 + 8

"""
reg_num = memory[2]
value = memory[3]
register[1] = memory[3]

"""
print(register) #[0, 37, 0, 0, 0, 0, 0, 0]