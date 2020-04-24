#!/usr/bin/env python

"""Main."""

import sys
from cpu import CPU


def run_cpu(filename, debug):
	try:
		cpu = CPU(debug=debug)

		cpu.load(filename)
		cpu.run()
	except (Exception, KeyboardInterrupt):
		cpu.trace()
		raise


if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print('Usage: python3 ls8.py filename.ls8 [-d]')
		sys.exit()
	filename = sys.argv[1]
	debug = True if '-d' in sys.argv or '--debug' in sys.argv else False
	run_cpu(filename, debug)
