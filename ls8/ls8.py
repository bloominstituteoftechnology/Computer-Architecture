#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
if len(sys.argv) != 2:
    print('Usage: file.py filename')
    sys.exit(1)
filename = sys.argv[1]

cpu = CPU()

cpu.load(filename)
cpu.run()