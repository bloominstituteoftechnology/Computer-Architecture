#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load(sys.argv[1]) #(file_name_from_command_line)
cpu.run()