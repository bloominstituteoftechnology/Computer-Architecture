#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

mult = [
    0b10000010, # LDI R0,8
    0b00000000,
    0b00001000,
    0b10000010, # LDI R1,9
    0b00000001,
    0b00001001,
    0b10100010, # MUL R0,R1
    0b00000000,
    0b00000001,
    0b01000111, # PRN R0
    0b00000000,
    0b00000001# HLT
]

cpu = CPU()

cpu.load(mult)
cpu.run()