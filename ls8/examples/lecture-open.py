import sys

# print(sys.argv[0])
try:
    with open(sys.argv[1]) as my_file:
        for line in my_file:
            comment_split = line.split("#")
            maybe_binary_number = comment_split[0]

            try:
                x = int(maybe_binary_number, 2)
                print("{:08b}: {:d}".format(x,x))
            except:
                print(f"failed to cast {maybe_binary_number} as an integer")
                continue
except FileNotFoundError:
    print("file not found")