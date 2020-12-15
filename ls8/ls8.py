#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

if len(sys.argv) != 2:
    print(f"Error from {sys.argv[0]}: {sys.argv[1]} not found")
    sys.exit(1)
else:
    file_name = sys.argv[1]

cpu.load(file_name)
cpu.run()
