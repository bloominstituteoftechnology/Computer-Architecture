#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

if len(sys.argv) < 2:
    print("ERROR, MUST SPECIFY FILE")
prog_path = sys.argv[1]

cpu.load(prog_path)
cpu.run()