#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
# I think we will have to do sys.argv[3] or something into the load 
cpu.load()
cpu.run()