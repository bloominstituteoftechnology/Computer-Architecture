#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) == 2: # CPU file + file to be ran
    cpu = CPU()
    cpu.load(sys.argv[1]) # pass filename to run
    cpu.run()
else:
    print('Error: Please provide filename to execute instructions')
    sys.exit(1)
