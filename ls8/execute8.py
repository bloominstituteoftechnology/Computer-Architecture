#!/usr/bin/env python3

"""Main."""

import sys
from cpu     import *
from helpers import *

# Set a default input file
fname = "./examples/stack.ls8"
# Grab the command line arguments
args  = sys.argv
# Validate the line arguments
if len(args) > 1:
    # grab the filename from the arguments
    fname = args[1]

#* Open the file
try:
    # print("Open file: {fname}".format(fname=fname))
    fle = open(fname, 'r')
except:
    print("ERR: error opening input file - terminating")
    quit()

#* Read the file contents into a list
try:
    lines = fle.readlines()
    # print("INF: read in {num_lines}".format(num_lines=len(lines)))
except:
    print("ERR: error reading the input file - terminating")
    quit()

#* Iterate through the list of instructions
instructions = []
for lne in lines:
    # Skip non instruction lines
    if lne[0] == "#":
        # skip a standard comment line
        continue

    if len(lne) < 8:
        # skip a short line (e.g. whitespace)
        continue
    # generate a binary instruction from the line
    #   being iterated on
    instr = genInt(lne[:8])
    instructions.append(instr)

cpu = CPU()

cpu.load(instructions)
cpu.run()

