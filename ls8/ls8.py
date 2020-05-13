#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

# from examples import print8


program = [
    0b10000010, # LDI R0,8
    0b00000000,
    0b00001000,
    0b01000111,# PRN R0
    0b00000000,
    0b00000001 # HLT

]


cpu = CPU()

cpu.load(sys.argv[1])
cpu.run()