#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python3 ls8.py <filename>", sys.argv)
        exit(0)

    #Read the program from file
    fileWithData = sys.argv[1]
    program = []
    with open(fileWithData) as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or len(line) == 0: #Skip comment and blank line
                continue
            print(line)
            x = line.split("#")
            program.append(int(x[0].strip(), 2))
    print("Returning program as ", program)

    cpu = CPU()

    cpu.load(program) #Load the program in memory
    cpu.run()  #Run the CPU to execute the program