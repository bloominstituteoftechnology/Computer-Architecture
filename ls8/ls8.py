#!/usr/bin/env python3

"""Main."""

import sys
# print(sys.argv)
from cpu import *

cpu = CPU()

cpu.load(sys.argv[1])
cpu.run()