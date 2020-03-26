#!/usr/bin/env python3

"""Main."""

import sys
from cpu import CPU

cpu = CPU()

cpu.load(sys.argv[1])
cpu.run()