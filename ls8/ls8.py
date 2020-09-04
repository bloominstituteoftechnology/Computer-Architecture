#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

print(f' >>>> sys.argv    {sys.argv} sys.argv')
print(f' sys.argv[1] is {sys.argv[1]} ')
cpu.load(sys.argv[1])
cpu.dump_mem('h')
cpu.run()