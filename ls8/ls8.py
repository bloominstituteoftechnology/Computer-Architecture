import sys
from cpu import *
from os import listdir
from os.path import isfile, join

examples = "./examples"
existing_files = [file for file in listdir(examples) if isfile(join(examples, file))]

if len(sys.argv) < 2 or len(sys.argv) > 2 or not sys.argv[1].endswith(".ls8"):
    print("USAGE: py ls8.py FILE_NAME.ls8")
    exit()
elif sys.argv[1] not in existing_files:
    print("Specified file not in /examples directory.")
    print("OPTIONS:")
    print(existing_files)
    exit()
else:

    file = open(join(examples, sys.argv[1]), "r")
    code = [int(line.strip().split('#',1)[0].strip(), 2) for line in file.readlines() if not line.startswith("#") and line.strip()]

    file.close()

    cpu = CPU()
    cpu.load(code)
    cpu.run()