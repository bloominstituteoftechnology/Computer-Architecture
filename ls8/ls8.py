#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

args = sys.argv
if len(args) == 2:
    cpu.load(args[1])
else:
    cpu.load()
    
cpu.run()