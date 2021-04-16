#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) != 2:
    print("Usage: python3 fileio.py <filename>")
    sys.exit(1)

try:
    with open(sys.argv[1]) as f:
        for line in f:
            print(int(line))

except FileNotFoundError:
    print("file not found")
    sys.exit(2)

cpu = CPU()

cpu.load(filename)
cpu.run()