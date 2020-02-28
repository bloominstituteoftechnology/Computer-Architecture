import sys

print(sys.argv)

if len(sys.argv) != 2:
    print("Error: Must have file name")
    sys.exit(1)

try:
    #open file
    with open(sys.argv[1]) as f:
        #read all lines
        for line in f:
            #ignore comments
            commentSplit = line.strip().split("#")
            value = commentSplit[0].strip()
            #ignore blank lines
            if value == "":
                continue
            #cast to numbers
            num = int(value)
            print(num)
except FileNotFoundError:
    print("File not found")
    sys.exit(2)
