#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

def main(argv):
	"""Main."""

	if len(argv) != 2:
		print(f"usage: {argv[0]} filename", file=sys.stderr)
		return 1

	cpu = CPU()
	cpu.load(argv[1])
	cpu.run()


if __name__ == "__main__":
	sys.exit(main(sys.argv))