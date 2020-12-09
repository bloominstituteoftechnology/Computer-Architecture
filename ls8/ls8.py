#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

# From class
""" if(len(sys.argv) != 2):
    print('Please pass two arguments')
else:
    console_args = sys.argv[1]
    cpu = CPU()
    cpu.load(console_args)
    cpu.run() """
##############

console_args = sys.argv[1]
cpu = CPU()
cpu.load(console_args)
cpu.run()