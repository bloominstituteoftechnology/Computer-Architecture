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

running = True

while running:
    inst = memory[pc]

    if inst == 1:  # PRINT_BEEJ
        print("Beej")
        pc += 1

    elif inst == 2:  # HALT
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

    else:
        print(f"Unknown instruction {inst}")
        running = False

