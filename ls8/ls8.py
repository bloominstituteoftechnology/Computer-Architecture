#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
# I think we will have to do sys.argv[1] or something into the load 
filename = sys.argv[1]
cpu.load(filename)
cpu.run()