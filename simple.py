import sys

PRINT_BEEJ  = 1
HALT        = 2
PRINT_NUM   = 3

memory = [
    PRINT_BEEJ,
    PRINT_BEEJ,
    PRINT_BEEJ,
    HALT
]

pc = 0 # program counter

while True:
    command = memory[pc]

    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1
    elif command == HALT:
        sys.exit(0)
    else:
        print("I did not understand that command")
