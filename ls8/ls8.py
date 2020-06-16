#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

program = [
    # 0b10000010, # LDI R0,8
    # 0b00000000,
    # 0b00001000,
    # 0b10000010, # LDI R1,9
    # 0b00000001,
    # 0b00001001,
    # 0b10100010, # MUL R0,R1
    # 0b00000000,
    # 0b00000001,
    # 0b01000111, # PRN R0
    # 0b00000000,
    # 0b00000001# HLT
]

file_name = sys.argv[1]
with open(file_name) as f:
    lines = f.readlines()
    for line in lines:
        if line[0]!= '#':
            num = int(line[0:8], 2)
            program.append(num)
# print(program)
print(program)
cpu = CPU()

cpu.load(program)
cpu.run()