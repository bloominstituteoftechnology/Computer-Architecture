#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
from os import listdir
from os.path import isfile, join

examples = "./examples"
existing_files = [file for file in listdir(examples) if isfile(join(examples, file))]

if len(sys.argv) < 2 or len(sys.argv) > 2 or not sys.argv[1].endswith(".ls8"):
    print("USAGE: py ls8.py FILE_NAME.ls8")
    # exit()
elif sys.argv[1] not in existing_files:
    print("Specified file not in /examples directory.")
    print("OPTIONS:")
    print(existing_files)
    # exit()
else:

    file = open(join(examples, sys.argv[1]), "r")

    # Get rid of everything that is a comment.
    # If The line begins with # get rid of it
    # If after running .strip() the string is empty, get rid of it
    # For the rest of the lines:
    # - Use .strip() to get rid of special characters
    # - use .split() to separate everything after "#" and take out only index 0
    # - use .strip() again to get rid of any left over spaces
    # And after all is said and done, conver the left-over string into an int with base 2
    code = [int(line.strip().split('#',1)[0].strip(), 2) for line in file.readlines() if not line.startswith("#") and line.strip()]

    file.close()

    cpu = CPU()
    cpu.load(code)
    cpu.run()

# file = open(join(examples, "print8.ls8"), "r")
# code = [int(line.strip().split('#',1)[0].strip(), 2) for line in file.readlines() if not line.startswith("#") and line.strip()]
# print(code)
# file.close()
# cpu = CPU()
# cpu.load(code)
# cpu.run()