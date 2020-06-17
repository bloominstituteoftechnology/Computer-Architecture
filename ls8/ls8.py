#!/usr/bin/env python3

"""Main."""

import sys
prog = sys.argv[1]


    
from cpu import *

cpu = CPU()

cpu.load(prog)
cpu.run()
