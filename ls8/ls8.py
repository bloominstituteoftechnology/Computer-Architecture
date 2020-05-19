#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *


file = open(sys.argv[1], "r")

program = []

for line in file:
    line = line.split(' ')[0]
    line = line.split('#')[0]
    if len(line) >= 8:
        program.append(int(line, 2))

file.close()

cpu = CPU()

cpu.load(program)
cpu.run()