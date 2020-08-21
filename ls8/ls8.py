#!/usr/bin/env python3

"""Main."""

from cpu import *

cpu = CPU()

cpu.load('examples/sctest.ls8')
cpu.run()
