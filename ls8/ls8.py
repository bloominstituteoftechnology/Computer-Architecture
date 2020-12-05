#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

console_args = sys.argv[1]

cpu = CPU()

cpu.load(console_args)
cpu.run()