import sys

# a simple data-driven machine that reads instructions out of memory and executes them.

PRINT_HI = 1
HALT = 2
PRINT_NUM = 3
SAVE = 4 # Save a value to a register
PRINT_REGISTER = 5 # Prints val of a register
ADD = 6 # adds values from two registers and stores it in one register

# pc = program counter that points to current instruction to execute.
pc = 0
running = True

memory = [
    PRINT_HI,
    SAVE,
    65,
    2,
    SAVE,
    20,
    3,
    ADD,
    2,
    3,
    PRINT_REGISTER,
    2,
    HALT
]

# acutal hardware in computers. Accessing values are extremely fast, and are for frequent operations.
register = [0] * 8

while running:
    command_to_execute = memory[pc]

    if command_to_execute == PRINT_HI:
        print("hi")
    elif command_to_execute == HALT:
        running = False
    elif command_to_execute == PRINT_NUM:
        pc += 1
        print(memory[pc])
    elif command_to_execute == SAVE:
        register[memory[pc+2]] = memory[pc+1]
        pc += 2
    elif command_to_execute == ADD:
        register[memory[pc+1]] = register[memory[pc+1]] + register[memory[pc+2]]
        pc += 2
    elif command_to_execute == PRINT_REGISTER:
        pc += 1
        print(register[memory[pc]])
    else:
        print("IDK")
        sys.exit(1)
    # goes to the next instruction
    pc += 1

