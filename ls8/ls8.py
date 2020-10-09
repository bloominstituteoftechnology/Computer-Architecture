#!/usr/bin/env python3

"""Main."""

import sys
import os
import re
from cpu import *

def main():
    if len(sys.argv) == 1:
        print('Please pass in an exmaple in the folowing format:')
        print('python3 ls8.py examples/mult.ls8')
    elif len(sys.argv) > 1:
        raw = sys.argv[1]
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), raw)

        cpu = CPU()

        with open(filepath, 'r') as f:
            lines = f.readlines()

            program = []

            for line in lines:
                val = line.split('#', 1)[0]
                val = val.split('\n', 1)[0]
                if len(val) > 0:
                    program.append(int(val, 2))

            cpu.load(program)
        f.close()
        cpu.run()


if __name__ == "__main__":
    main()