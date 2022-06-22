import sys

# auth code
PRINT_BEEJ = 1
HALT = 2
PRINT_NUM = 3
# memory is basically an array of 1s and 0s
# RAM
memory = [
    PRINT_BEEJ,
    PRINT_NUM,
    56,
    PRINT_BEEJ,
    PRINT_NUM,
    34,
    PRINT_BEEJ,
    HALT
]

pc = 0
running = True


# processor
while running:
    command = memory[pc]

    if command == PRINT_BEEJ:
        print("Beej!")
        pc +=1

    elif command == HALT:
        running = False
        pc += 1

    elif command == PRINT_NUM:
        num = memory[pc + 1]
        print(num)
        pc += 2

    else:
        print("Unknown instruction: {command}")
        sys.exit(1)
        pc += 1
