#!/usr/bin/env python

"""Main."""

import sys
from cpu import CPU

cpu = CPU(debug=False)

cpu.load()
cpu.run()
