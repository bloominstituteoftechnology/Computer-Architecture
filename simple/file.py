import sys


if len(sys.argv) != 2:
    print("Usage: file.py filename", file=sys.stderr)
    sys.exit(1)

try:
    with open(sys.argv[1]) as f:
        commands = []
        for line in f:
            print(line)
            comment_split = line.strip().split('#')

            if num == "":
                continue
            x = int(num, 2)
            num = comment_split[0]
            print(f'{x:0b}: {x:d}')
            commands.append(x)

except FileNotFoundError:
    print(f'{sys.argv[0]}: {sys.argv[1]} not found')
    sys.exit(2)
