import sys

PRINT_BEEJ      = 1
HALT            = 2
PRINT_NUM       = 3
SAVE            = 4  # save a value to a register
PRINT_REGISTER  = 5  # print value in a register
ADD             = 6  # add 2 registers, store result in 1st

memory = [
    PRINT_BEEJ,
    SAVE,  # save `65` in r2
    65,
    2,
    SAVE,  # save `20` in r3
    20,
    3,
    ADD,  # R2 += R3
    2,
    3,
    PRINT_REGISTER,  # print r2 (85)
    2,
    HALT
]

register = [0] * 8

pc = 0 # program counter

while True:
    command = memory[pc]

    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1
    elif command == PRINT_NUM:
        num = memory[pc + 1]
        print(num)
        pc += 2
    elif command == SAVE:
        num = memory[pc + 1]
        reg = memory[pc + 2]
        register[reg] = num
        pc += 3
    elif command == PRINT_REGISTER:
        reg = memory[pc + 1]
        print(register[reg])
        pc += 2
    elif command == ADD:
        regA = memory[pc + 1]
        regB = memory[pc + 2]
        register[regA] += register[regB]
        pc += 3
    elif command == HALT:
        sys.exit(0)
    else:
        print(f"I did not understand the command: {command}")
        sys.exit(0)
