"""
Computer emulator

Software that pretends to be hardware

Turing Complete -- it can solve any problem for which there is an algorithm.

256bytes in total

Write a program that can run any program.
- add this to your resume.
"""

# Memory = an array
# Index in the array and value that is stored there
"""
Memory --like a big array
Index into the memory array" =="address" == "pointer"
"""

# a = [1, 2, 3]
#
# print(a[0])
# a[0] = 99

# memory = [0] * 256 #RAM

import sys
PRINT_JORGE = 1
HALT = 2
SAVE_REG = 3  # SAVE_REG R1, 37
PRINT_REG = 4  # PRINT_REG R1

# running instructions
memory = [
    PRINT_JORGE,  # < ---- PC
    # PRINT_JORGE,
    # PRINT_JORGE,
    # SAVE_REG R1, 37
    1,
    # 37,
    99,
    SAVE_REG,
    2,
    11,
    ADD,  # ADD R1, R2 register[1] += register[2]
    1,
    2,
    PRINT_REG,
    1,
    PRINT_JORGE,
    HALT,
]

register = [0] * 8  # 8 registers, like variables. We have 8 here, RO, R1, R2 .. R7
pc = 0  # Program Counter, index of the current instruction
running = True

# for v in memory:
while running:
    ir = memory[pc]  # Instruction register = ir
    # if v == PRINT_JORGE:
    if ir == PRINT_JORGE:
        print("Jorge !")
        pc += 1
    # elif v == HALT:
    # elif ir == HALT:
    elif ir == SAVE_REG:
        reg_num = memory[pc + 1]  # grab it out of memory
        reg_num = memory[pc + 2]
        register[reg_num] = value
        # break
        running = False
        pc += 3
    elif ir == HALT
    running = False
    pc += 1
    else:
        print(f"Unkown instruction {ir} at address {pc}")
        sys.exit
