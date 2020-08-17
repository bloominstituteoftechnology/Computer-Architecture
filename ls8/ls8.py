#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

print(sys.argv)

cpu = CPU()

cpu.load()
cpu.run()