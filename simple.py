import sys

PRINT_BEEJ     = 1
HALT           = 2
PRINT_NUM      = 3 
SAVE           = 4  # Save a value to a register
PRINT_REGISTER = 5  # Print the value in a register
ADD            = 6  # Add 2 registers, store the result in 1st reg
PUSH           = 7
POP            = 8

memory = [
    PRINT_BEEJ,
    SAVE,
    65,
    2,
    SAVE,
    20,
    3,
    ADD,
    2,
    3,
    PRINT_REGISTER,
    2,
    HALT
]

memory = [0] * 256
register = [0] * 8

SP = 7

pc = 0 # Program counter

def load_memory(filename):
    try:
        address = 0
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
                num = int(value)
                # populate a memory array
                memory[address] = num
                address += 1
                
                # print(f"{num:08b}: {num}")

    except FileNotFoundError:
        print("File not found")
        sys.exit(2)

if len(sys.argv) != 2:
    print("ERROR: must have file name")
    sys.exit(1)

load_memory(sys.argv[1])

print(memory)

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
        reg_a = memory[pc + 1]
        reg_b = memory[pc + 2]
        register[reg_a] += register[reg_b]
        pc += 3
    elif command == PUSH:
        # Grab the register argument
        reg = memory[pc + 1]
        val = register[reg]
        # Decrement the SP.
        register[SP] -= 1
        # Copy the value in the given register to the address pointed to by SP.
        memory[register[SP]] = val
        pc += 2
    elif command == POP:
        # Grab the value from the top of the stack
        reg = memory[pc + 1]
        val = memory[register[SP]]
        # Copy the value from the address pointed to by SP to the given register.
        register[reg] = val
        # Increment SP.
        register[SP] += 1
        pc += 2
    elif command == HALT:
        sys.exit(0)
    else:
        print(f"I did not understand that command {command}")
        sys.exit(1)