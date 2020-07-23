# # This doesn't close the file
# file = open('print8.ls8', 'r')
# lines = file.read()
# print(lines)

import sys

if len(sys.argv) < 2:
    print("Please pass in a second filename: python in_and_out.py second_filename.py")
    sys.exit()


file_name = sys.argv[1]

## This closes the file after reading
try:
    with open(file_name) as file:
        for line in file:
            split_line = line.split('#')[0]
            command = split_line.strip()
            if command != '':
                print(int(command, 2))
except FileNotFoundError:
    print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
    sys.exit()