#!/usr/bin/env python

import sys

PRINT_BEEJ = 1
HALT = 2
PRINT_NUM = 3
SAVE = 4# save value into register
PRINT_REGISTER = 5
ADD = 6
PUSH = 7
POP = 8


memory = [0] * (2**8)
pc = 0
running = True

if len(sys.argv) != 2:
    print("usage: fileio.py <filename>", file=sys.stderr)
    sys.exit(1)

# create 8 registers
register = [0] * 8

SP = 7

def load_memory(filename):
    global memory
    address = 0
    try:
        with open(filename) as f:
            for line in f:
                # process comments: ignore anything after a #
                comment_split = [x for x in line.split("#") if x!='']
                #convert numbers from strings binary to integers.
                try:
                    num = comment_split[0].strip()
                    x = int(num)
                    memory[address] = x
                    address += 1
                except ValueError as e:
                    # print(f"WARNING: {e}")
                    continue
                except IndexError as e:
                    print(f"WARNING: {e}")
                    continue

                #print(f"{x:08b}: {x}")
    except FileNotFoundError:
        print(f"{sys.argv[0]}: {sys.argv[1]} not found")
        sys.exit(2)

load_memory(sys.argv[1])

#for byte in memory[:30]:
#    print(byte)


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

    elif command == PUSH:
        reg = memory[pc + 1]
        val = memory[reg]
        #Decrement the SP.
        register[SP] -= 1
        # Copy the value in the given register to the address pointed to by SP.
        memory[register[SP]] = val
        pc += 2

    elif command == POP:
        reg = memory[pc + 1]
        val = memory[register[SP]]
        # Copy the value from the address pointed to by SP to the given register.
        register[reg] = val
        # Increment SP.
        register[SP] += 1
        pc += 2

        
    else:
        print(f"unknown instruction: {command}")
        sys.exit(1)

"""
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

"""
