"""
CPU
    Executing instructions
    Gets them out of RAM
    Registers (like variables)
        Fixed names  R0-R7
        Fixed number of them -- 8 of them
        Fixed size -- 8 bits

Memory (RAM)
    A big array of bytes
    Each memory slot has an index, and a value stored at that index
    That index into memory AKA:
        pointer
        location
        address
"""
import sys

memory = [0] * 256

address = 0

if len(sys.argv) != 2:
    print("usage: comp.py filename")
    sys.exit(1)

try:
    with open(sys.argv[1]) as f:
        for line in f:
            try:
                line = line.split("#",1)[0]
                line = int(line, 10)  # int() is base 10 by default
                memory[address] = line
                address += 1
            except ValueError:
                pass

except FileNotFoundError:
    print(f"Couldn't find file {sys.argv[1]}")
    sys.exit(1)

register = [0] * 8

pc = 0  # Program Counter, index into memory of the current instruction
        # AKA a pointer to the current instruction

fl = 0

SP = 7

register[SP] = 0xf4

PRINT_BEEJ = 1
HALT = 2

running = True

while running:
    inst = memory[pc]

    if inst == PRINT_BEEJ:
        print("Beej")
        pc += 1

    elif inst == HALT:
        running = False

    elif inst == 3:  # SAVE_REG
        reg_num = memory[pc + 1]
        value = memory[pc + 2]

        register[reg_num] = value

        pc += 3

    elif inst == 4: # PRINT_REG
        reg_num = memory[pc + 1]
        print(register[reg_num])

        pc += 2

    elif inst == 5:  # PUSH
        # decrement stack pointer
        register[SP] -= 1

        register[SP] &= 0xff  # keep R7 in the range 00-FF

        # get register value
        reg_num = memory[pc + 1]
        value = register[reg_num]

        # Store in memory
        address_to_push_to = register[SP]
        memory[address_to_push_to] = value

        pc += 2

    elif inst == 6:  # POP
        # Get value from RAM
        address_to_pop_from = register[SP]
        value = memory[address_to_pop_from]

        # Store in the given register
        reg_num = memory[pc + 1]
        register[reg_num] = value

        # Increment SP
        register[SP] += 1

        pc += 2

    else:
        print(f"Unknown instruction {inst}")
        running = False

