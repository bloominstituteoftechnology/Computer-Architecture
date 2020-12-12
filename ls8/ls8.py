#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

try:
    filename = sys.argv[1]
    with open(filename) as f:
        cpu.load(filename)
        cpu.run()
except IndexError:
    print("Please provide an input")
except FileNotFoundError:
    print(f"Error from {sys.argv[0]}: {sys.argv[1]} not found")