
PRINT_TIM    =  0b00000001
HALT         =  0b10  # 2
PRINT_NUM    =  0b00000011  # opcode 3
SAVE         =  0b100
PRINT_REG    =  0b101    # opcode 5
ADD          =  0b110


# registers[2] = registers[2] + registers[3]

# memory = [
#     PRINT_TIM,
#     PRINT_TIM,
#     PRINT_NUM,
#     42,
#     SAVE,
#     2,       # register to put it in
#     99,      # number to save
#     SAVE,
#     3,      # register to save in
#     1,      # number to save
#     ADD,
#     2,   # register to look at, and save stuff in
#     3,   # register to look at
#     PRINT_REG,
#     2,       # register to look at
#     HALT,
# #           ]

import sys

memory = [0] * 256 

def load_memory(file_name):
    try:
        address = 0
        with open(file_name) as file:
            for line in file:
                split_line = line.split('#')[0]
                command = split_line.strip()

                if command == '':
                    continue

                instruction = int(command, 2)
                memory[address] = instruction

                address += 1

    except FileNotFoundError:
        print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
        sys.exit()

if len(sys.argv) < 2:
    print("Please pass in a second filename: python3 in_and_out.py second_filename.py")
    sys.exit()

file_name = sys.argv[1]
load_memory(file_name)

# write a program to pull each command out of memory and execute
# We can loop over it!

# register aka memory
registers = [0] * 8
# [0,0,99,0,0,0,0,0]
# R0-R7


pc = 0  # program counter
running = True
while running:
    command = memory[pc]

    if command == PRINT_TIM:
        print("Tim!")

    if command == HALT:
        running = False

    if command == PRINT_NUM:
        num_to_print = memory[pc + 1]
        print(num_to_print)
        pc += 1

    if command == SAVE:
        reg = memory[pc + 1]
        num_to_save = memory[pc + 2]
        registers[reg] = num_to_save

        pc += 2

    if command == PRINT_REG:
        reg_index = memory[pc + 1]
        print(registers[reg_index])
        pc += 1

    if command == ADD:
        first_reg = memory[pc + 1]
        sec_reg = memory[pc + 2]
        registers[first_reg] = registers[first_reg] + registers[sec_reg]
        pc += 2

    pc += 1