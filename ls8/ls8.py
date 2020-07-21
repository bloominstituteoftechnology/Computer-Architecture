#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

file_name = sys.argv[1]

cpu.load(file_name)
cpu.run()