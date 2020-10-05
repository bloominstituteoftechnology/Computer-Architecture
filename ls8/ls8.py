#!/usr/bin/env python3

"""Main."""

argv_err_msg = """
Error: You must specify a file name as a command line argument.
This file should contain the binary instruction set you want the CPU to run.

    Ex: python3 ls8.py examples/print8.ls8
"""

import sys
from cpu import *
import os.path

cpu = CPU()

# cd S7-Computer-Architecture/M1-4/Computer-Architecture/ls8
# python3 ls8.py examples/print8.ls8
# python3 ls8.py examples/mult.ls8
if len(sys.argv) != 2:
    # file_name = os.path.join(os.path.dirname(__file__), "examples/mult.ls8")
    print(argv_err_msg)
    sys.exit(1)
else:
    file_name = os.path.join(os.path.dirname(__file__), sys.argv[1])

program = []
try:
    with open(file_name) as f:
        for line in f:
            num = line.split("#")[0]
            try:
                program.append(int(num, 2))
            except:
                continue
except:
    print(f'Could not find file named: {file_name}')
    sys.exit(1)

cpu.load(program)
cpu.run()