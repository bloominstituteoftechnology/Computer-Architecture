import sys

# The index into the memory array, AKA location, address, pointer

# 1 - PRINT_AARON
# 2 - HALT
# 3 - SAVE_REG  store a value in a register
# 4 - PRINT_REG  print the register value in decimal

memory = [0] * 256   # think of as a big array of bytes, 8-bits per byte

registers = [0] * 8

# Load the program file
address = 0

if len(sys.argv) != 2:
    print("usage: comp.py progname")
    sys.exit(1)

try:
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.strip()
            temp = line.split()

            if len(temp) == 0:
                continue

            if temp[0][0] == '#':
                continue

            try:
                memory[address] = int(temp[0])

            except ValueError:
                print(f"Invalid number: {temp[0]}")
                sys.exit(1)

            address += 1

except FileNotFoundError:
    print(f"Couldn't open {sys.argv[1]}")
    sys.exit(2)

if address == 0:
    print("Program was empty!")
    sys.exit(3)

# print(memory[:10])
# sys.exit(0)


running = True

pc = 0   # Program Counter, the index into memory of the currently-executing instruction

while running:
    ir = memory[pc]  # Instruction Register

    if ir == 1:  # PRINT_BEEJ
        print("Aaron!")
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

    else:
        print(f"Invalid instruction {ir} at address {pc}")
        sys.exit(1)
