#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

if len(sys.argv) != 2:
    print("Usage: ls8.py filename.ls8")
    sys.exit()

path = sys.argv[1]

cpu.load(path)
cpu.run()