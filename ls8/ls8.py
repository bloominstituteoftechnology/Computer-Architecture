#!/usr/bin/env python3

"""Main."""

argv_err_msg = """
Error: You must specify a file Name as a command line argument
This file you specify should contain a binary instruction set to load into the CPU

Examples:
    python3 ls8.py examples/print8.ls8
    python3 ls8.py examples/mult.ls8
    python3 ls8.py examples/stack.ls8
    python3 ls8.py examples/call.ls8
"""

import sys
from cpu import *

project_day_num = 2

file_names = [
            "examples/print8.ls8",        # 0 - Day 1
              "examples/mult.ls8",          # 1 - Day 2
              "examples/stack.ls8",         # 2 - Day 3
              "examples/call.ls8",          # 3 - Day 4
              "examples/stackoverflow.ls8", # 4
              "examples/interrupts.ls8",    # 5
              "examples/keyboard.ls8",      # 6
              "examples/printstr.ls8",      # 7
              "examples/sctest.ls8", ]      # 8

file_name = file_names[project_day_num - 1]


if len(sys.argv) != 2:
    # print(f'\nRunning file: {file_name}')
    print(argv_err_msg)
    sys.exit(1)

else:
    file_name = sys.argv[1]



cpu = CPU()
cpu.load(file_name)
cpu.run()
print()