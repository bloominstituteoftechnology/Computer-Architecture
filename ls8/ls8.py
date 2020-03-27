#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

if sys.argv[2] == "debug":
    debug = True
else:
    debug = False

cpu.load(sys.argv[1])
cpu.run(debug=debug)