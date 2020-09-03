#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
print('reg:', cpu.reg, 'ram', cpu.ram)
cpu.load()
cpu.run()

print('binary list access:', cpu.ram)
