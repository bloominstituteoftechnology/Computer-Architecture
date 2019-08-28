#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

#if sys arguments are incorrect print error and exit
if len(sys.argv) != 2:
   print("please provide filename")
   print(sys.stderr)
   sys.exit(1)
#create CPU, load with instructions, and run
else:
   cpu = CPU()
   cpu.load()
   cpu.run()