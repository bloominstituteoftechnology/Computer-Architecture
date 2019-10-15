#!/usr/bin/env python3

"""Main."""

import sys
from argparse import ArgumentParser
from cpu import CPU

parser = ArgumentParser(description="select a file of ls8 code to run")
parser.add_argument('filename', type=str, help="select a filename")

if __name__=='__main__':
    args = parser.parse_args()
    cpu = CPU()

    cpu.load(args.filename)
    cpu.run()
