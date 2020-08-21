#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
# I think we will have to do sys.argv[1] or something into the load 
if len(sys.argv) < 2:
    print("Please enter filename after module in command line")
    print("Example: python ls8.py examples/mult.ls8")
    sys.exit()
filename = sys.argv[1]
cpu.load(filename)
cpu.run()