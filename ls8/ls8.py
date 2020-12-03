#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) != 2:
    print(argv_err_msg)
    sys.exit(1)
else:
    # cd ../S7-Computer-Architecture/M1-4/Computer-Architecture/ls8
    # python3 ls8.py examples/print8.ls8
    file_name = sys.argv[1]

cpu = CPU()
cpu.load(file_name)
cpu.run()