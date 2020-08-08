#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load()
cpu.run()

# Get print8.ls8 running


# Step 0: IMPORTANT: inventory what is here!
# Make a list of files here.
# #  CPU.PY,

# Note what has been implemented, and what hasn't.
# For step 1: Done
# # Added self.ram = [None] * 8 # 8 general-purpose registers.
        # and self.memory = 0 # to hold 256 bytes of memory

        # kinda of confused if I use ram or reg
        # ram for the 256 bytes, reg for the 8 registers?
        # if so, why
        # for instruction in program:
            # self.ram[address] = instruction
            # address += 1
#

