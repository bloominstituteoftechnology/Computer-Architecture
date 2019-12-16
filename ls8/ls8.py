#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU(8,8)

cpu.load()
cpu.run()