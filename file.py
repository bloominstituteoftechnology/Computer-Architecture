# take an argument, load the values from that file and put it in an array

import sys


print(sys.argv)


if len(sys.argv) != 2:
    print("ERROR: must have file name")
    sys.exit(1)

try:
    # open the file
    with open(sys.argv[1]) as f:
        # Read all the lines
        for line in f:
            # Parse out the comments
            comment_split = line.strip().split("#")

            # cast the numbers from strings to ints
            value = comment_split[0].strip()
            # ignore blank lines
            if value == "":
                continue
            num = int(value, 2)
            # populate a memory array
            memory[mem_address] = num
            mem_address += 1
            
            print(f"{num:08b}: {num}")

except FileNotFoundError:
    print("File not found")
    sys.exit(2)

