#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

if len(sys.argv) != 2:
    print('usage cpu.py')
    sys.exit(1)

cpu.load()
cpu.run()
