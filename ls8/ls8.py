#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

if len(sys.argv) < 2:
    print("Please pass a second filename: python3 file_one.py file_two.py")
    sys.exit()

file_name = sys.argv[1]

cpu.load(file_name)
cpu.run()


