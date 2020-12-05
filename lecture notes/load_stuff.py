import sys

# file i/o in Python

# read a file, in Python?

# try:
#     file = open("print8.ls8", 'r')
#     lines = file.read()

#     # print(lines)

#     # imagine we go do a billion things here
#     # file will still be open

#     # and will still be open if we hit an Exception
#     raise Exception('hi')

# except Exception:
#     print(file.closed)

try:
    if len(sys.argv) < 2:
        print(f'Error from {sys.argv[0]}: missing filename argument')
        print(f'Usage: python3 {sys.argv[0]} <somefilename>')
        sys.exit(1)

    with open(sys.argv[1]) as f:
        
        # lines = f.readlines()
        # for line in lines:
        #     if line[0] != "#" and line[0] != '\n':
        #    take [:8] characters of string
        #   then use int()

        for line in f:
            split_line = line.split("#")[0]
            stripped_split_line = split_line.strip()

            if stripped_split_line != "":
                command = int(stripped_split_line, 2)

                print(command)

# except FileNotFoundError:
#     print(f'Your file {sys.argv[1]} was not found by {sys.argv[0]}')

except FileNotFoundError:
    print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
    print("(Did you double check the file name?)")

# read in the filename from the command line
## check that the file exists

# print(sys.argv) 