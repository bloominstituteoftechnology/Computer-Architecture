import sys

def loadFile(path):
    totalProgram = []
    try:
        with open(path) as file:
            for line in file:
                # ignore comments
                commentSplit = line.strip().split("#")
                command = commentSplit[0]

                if command == "":
                    continue

                # cast to numerical value
                num = int(command, 2)
                totalProgram.append(num)
    except FileNotFoundError:
        print("File not found")
        sys.exit(2)
    return totalProgram
