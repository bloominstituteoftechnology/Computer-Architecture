#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

def main(argv):

    if len(argv) != 2:
        print("usage: .ls8 filename")
        return 1

    cpu = CPU()

    cpu.load(argv[1])
    cpu.run()

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
