#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

# file_name_from_command_line = sys.argv[1]
file_name_from_command_line = 'mult.ls8'
print(file_name_from_command_line)


cpu.load(f"ls8/examples/{file_name_from_command_line}")
# cpu.load(file_name_from_command_line)
cpu.run()