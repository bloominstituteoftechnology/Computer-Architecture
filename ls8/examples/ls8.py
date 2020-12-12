#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

# # Mario's implementation
# if len(sys.argv) != 2:
#     print("Wrong number of arguments!")

# else:
#     cpu = CPU()
#     cpu.load(sys.argv[1])
#     cpu.run()
# ----------

cpu = CPU()

# file_name_from_command_line = sys.argv[1]
file_name_from_command_line = 'stack.ls8'
print(file_name_from_command_line)


cpu.load(f"ls8/examples/{file_name_from_command_line}")
# cpu.load(file_name_from_command_line)
cpu.run()