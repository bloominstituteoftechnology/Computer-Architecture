#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load("print8.ls8")
cpu.run()
print(f"Length of reg: {len(cpu.reg)}")