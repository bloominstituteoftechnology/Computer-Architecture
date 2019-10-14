#!/usr/bin/env python

import sys

PRINT_BEEJ = 1
HALT = 2
PRINT_NUM = 3
SAVE = 4# save value into register
PRINT_REGISTER = 5
ADD = 6

# 0000 0001 0000 0001 0000 0001 0000 0001 0000 0001 0000 0010
memory0 = [
    PRINT_BEEJ,
    PRINT_NUM,
    1,
    PRINT_NUM,
    12,
    PRINT_BEEJ,
    PRINT_NUM,
    37,
    PRINT_BEEJ,
    HALT
]

memory = [
    PRINT_BEEJ,
    SAVE, # save 65 into r2
    65,
    2,
    SAVE, # save 20 into R3
    20,
    3,
    ADD, # add R2 + R3 = 65 + 20, store in register 2
    2,
    3,
    PRINT_REGISTER,
    2,
    HALT
]

pc = 0
running = True

# create 8 registers
register = [0] * 8

while running:
    # do stuff
    command = memory[pc]
    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1
    elif command == PRINT_NUM:
        pc +=1
        num = memory[pc]
        print(num)
    elif command == HALT:
        running = False

    elif command == SAVE:
        num = memory[pc+1] # get num from first arg
        reg = memory[pc+2] # get register index from 2nd arg
        register[reg] = num # store the num in the correct register
        pc += 3

    elif command == PRINT_REGISTER:
        reg = memory[pc+1]
        print(register[reg])
        pc += 1

    elif command == ADD:
        reg_a = memory[pc+1]
        reg_b = memory[pc+2]
        register[reg_a] += register[reg_b] # should be 85
        pc += 3

    else:
        print(f"unknown instruction: {command}")
        sys.exit(1)

