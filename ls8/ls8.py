#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

# cpu.load()
cpu.load(sys.argv[1])
# print('sys.argv[1]', sys.argv[1])
# cpu.run()
