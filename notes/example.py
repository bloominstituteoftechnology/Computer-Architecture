import sys

# op codes
# operation codes
PRINT_MATT = 1
HALT = 2
PRINT_NUM = 3
SAVE = 4
PRINT_REGISTER = 5
ADD = 6

print_matt_program = [
    PRINT_MATT,
    PRINT_MATT,
    PRINT_MATT,
    PRINT_MATT,
    HALT
]
print_some_nums = [
    PRINT_NUM,
    12,
    PRINT_NUM,
    15,
    PRINT_NUM,
    37,
    PRINT_MATT,
    HALT
]
save_num_to_reg = [
    SAVE,
    65,
    2,
    PRINT_REGISTER,
    2,
    HALT
]

add_numbers = [
    SAVE,  # save number 12 to reg 1
    12,
    1,
    SAVE,
    45,
    2,
    ADD,  # Reg 1 += reg 2 (add two values and store in reg 1)
    1,
    2,
    PRINT_REGISTER,
    1,
    HALT
]


memory = add_numbers


# basic computer
running = True
pc = 0
registers = [0] * 8

while running:
    # lets receive some commands, and execute
    command = memory[pc]

    # if command is PRINT_MATT
    # print out Matts name
    if command == PRINT_MATT:
        print('Matt')
        pc += 1

    # if command is HALT
        # shutdown
    elif command == HALT:
        running = False
        pc += 1

    elif command == PRINT_NUM:
        # look at the next line in memory
        # print the number thats in that spot
        num = memory[pc + 1]
        print(num)
        pc += 2
    # if command is nonrecognizable
        # lets crash
    elif command == SAVE:
        num_to_save = memory[pc + 1]
        register = memory[pc + 2]
        registers[register] = num_to_save
        pc += 3
    elif command == PRINT_REGISTER:
        register = memory[pc + 1]
        print(registers[register])
        pc += 2
    elif command == ADD:
        register1 = memory[pc + 1]
        register2 = memory[pc + 2]
        val1 = registers[register1]
        val2 = registers[register2]
        registers[register1] = val1 + val2
        pc += 3
    else:
        print(f'unknown instruction {command}')
        sys.exit(1)
