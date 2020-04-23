#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
from FileOpener import *

cpu = CPU()

if len(sys.argv) < 2:
    print("Usage: ls8.py [programToRun]")
    sys.exit(1)

program = loadFile(sys.argv[1])

cpu.load(program)
cpu.run()
