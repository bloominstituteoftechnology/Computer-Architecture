import sys

PRINT_BEEJ      = 1
HALT            = 2
PRINT_NUM       = 3
SAVE            = 4  # save a value to a register
PRINT_REGISTER  = 5  # print value in a register
ADD             = 6  # add 2 registers, store result in 1st

memory = [0] * 256

if len(sys.argv) != 2:
    print("Error: Must have file name")
    sys.exit(1)

def loadMemory(filename):
    memPointer = 0
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
                # print(num)

                memory[memPointer] = num
                memPointer += 1
    except FileNotFoundError:
        print("File not found")
        sys.exit(2)

loadMemory(sys.argv[1])

register = [0] * 8

pc = 0 # program counter



while True:
    command = memory[pc]

    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1
    elif command == PRINT_NUM:
        num = memory[pc + 1]
        print(num)
        pc += 2
    elif command == SAVE:
        num = memory[pc + 1]
        reg = memory[pc + 2]
        register[reg] = num
        pc += 3
    elif command == PRINT_REGISTER:
        reg = memory[pc + 1]
        print(register[reg])
        pc += 2
    elif command == ADD:
        regA = memory[pc + 1]
        regB = memory[pc + 2]
        register[regA] += register[regB]
        pc += 3
    elif command == HALT:
        sys.exit(0)
    else:
        print(f"I did not understand the command: {command}")
        sys.exit(0)
