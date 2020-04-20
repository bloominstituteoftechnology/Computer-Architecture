#!/usr/bin/env python3

"""Main."""

import sys
from cpu import CPU

cpu = CPU()
if len(sys.argv) != 2: 
    print("must have a file name")
    sys.exit(1)

cpu.load(sys.argv[1])
cpu.run()