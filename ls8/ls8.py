#!/usr/bin/env python3
# import sys

# """Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load(sys.argv[1])
cpu.run()
