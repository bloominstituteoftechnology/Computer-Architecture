#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load()
#  python3 ls8.py examples/print8.ls8
if len(sys.argv) != 2:
    print(argv_err_msg)
    sys.exit(1)

program = []
file_name = sys.argv[1]
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