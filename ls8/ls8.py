#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
cpu.load(fileNameFromCommandLine)
cpu.run()
