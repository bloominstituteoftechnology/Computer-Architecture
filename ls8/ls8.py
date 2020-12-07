#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

try:
    filename = sys.argv[1]
    with open(filename) as f:
        cpu.load(filename)
        cpu.run()
except IndexError:
    print("please pass an input .ls8 file")
except FileNotFoundError:
    print("file not found.")

# cpu.load()
# cpu.run()