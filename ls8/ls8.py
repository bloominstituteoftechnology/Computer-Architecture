#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) > 1:
    with open(sys.argv[1]) as program_file:
        program = []
        for line in program_file.readlines():
            ir_str = line.strip().partition("#")[0]
            if len(ir_str) == 0:
                # there was a comment or blank line
                continue
            program.append(int(ir_str, 2))
    cpu = CPU()
    cpu.load(program)
    cpu.run()
else:
    print("Required argument: program file name")
        