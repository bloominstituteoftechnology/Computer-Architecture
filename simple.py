import sys

PRINT_BEEJ  = 1
HALT        = 2
PRINT_NUM   = 3

memory = [
    PRINT_BEEJ,
    PRINT_BEEJ,
    PRINT_BEEJ,
    PRINT_NUM,
    1,
    PRINT_NUM,
    12,
    HALT
]

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
    elif command == HALT:
        sys.exit(0)
    else:
        print(f"I did not understand the command: {command}")
        sys.exit(0)
