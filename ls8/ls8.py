#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *



register = [0] * 8

cpu = CPU()

cpu.load()
cpu.run()