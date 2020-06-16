#!/usr/bin/env python3

"""Main."""

import sys
import re
from cpu import *

cpu = CPU()
cpu.load("examples/mult.ls8")
cpu.run()

# prog_file = "examples/print8.ls8"
# prog = open(prog_file, "r")
# arr = []
# add = 0

# print("PROG: ", prog)

# for inst in prog:
#     # print("Inst: ", inst)
#     if "1" in inst and "0" in inst:
#         inst = re.findall(r'\d+', inst)
#         inst = inst[0]
#         print("INST: ", inst)
#         arr.append(inst)


# print("ARR :", arr)
