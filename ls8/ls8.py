#!/usr/bin/env python3

"""Main."""

argv_err_msg = """
Error: You must specify a file name as a command line argument.
This file you specify should contain a binary instruction set to load into the CPU.
    Examples:
        python3 ls8.py examples/print8.ls8
        python3 ls8.py examples/mult.ls8
        python3 ls8.py examples/stack.ls8
        python3 ls8.py examples/call.ls8
"""

import sys
from cpu import *

if len(sys.argv) != 2:
    print(argv_err_msg)
    sys.exit(1)
else:
    # cd ../S7-Computer-Architecture/M1-4/Computer-Architecture/ls8
    # python3 ls8.py examples/print8.ls8
    file_name = sys.argv[1]

cpu = CPU()
cpu.load(file_name)
cpu.run()
