#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

program = sys.argv[1]
cpu.load(program)

cpu.run()

print(cpu.ram[:15])