import sys

# op codes, this is what you would give a programmer as "documentation"
PRINT_ARTEM    = 1
HALT           = 2
PRINT_NUM      = 3
SAVE           = 4
PRINT_REGISTER = 5
ADD            = 6
POP            = 7
PUSH           = 8


# this is where we "initialize the memory"
memory = [0] * 256 

# ALL THE CODE BELOW IS THE "COMPUTER"
running = True
pc = 0
registers = [0] * 8
SP = 7 # register location that holds top of stack address
# store the top of memory into Register 7
registers[SP] = len(memory) - 1

# Read from file, and load into memory
# read the filename from command line arguments
# open the file, and load each line into memory
# lets try not to crash
def load_program_into_memory():
    address = 0
    # get the filename from arguments here
    print(sys.argv)
    if len(sys.argv) != 2:
        print("Need proper file name passed")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename) as f:
        for line in f:
            # print(line)
            if line == '':
                continue
            comment_split = line.split('#')
            # print(comment_split) # [everything before #, everything after #]

            num = comment_split[0].strip()

            memory[address] = int(num)
            address += 1



load_program_into_memory()
while running:
    # lets receive some instructions, and execute them
    command = memory[pc]

    # if command is PRINT_ARTEM
    if command == PRINT_ARTEM:
        # print out artem's name
        print('Artem!')
        pc += 1

    # if command is HALT
    elif command == HALT:
        running = False
        pc += 1
        # shutdown

    elif command == PRINT_NUM:
        # look at the next line in memory
        # print the number thats in that spot
        num = memory[pc + 1]
        print(num)
        pc += 2

    elif command == SAVE:
        # we expect to see two numbers after the instruction
        # number to save, and register location
        num_to_save = memory[pc + 1]
        register = memory[pc + 2]
        registers[register] = num_to_save
        pc += 3
    
    elif command == PRINT_REGISTER:
        # we expect to see one number after the instruction
        # number of register location
        register = memory[pc + 1]
        print(registers[register])
        pc += 2
    
    elif command == ADD:
        # we expect to see two numbers after the instruction
        # both register locations
        # we will save the result into the first register given to us
        register1 = memory[pc + 1]
        register2 = memory[pc + 2]
        val1 = registers[register1]
        val2 = registers[register2]
        registers[register1] = val1 + val2
        pc += 3
    elif command == PUSH:
        # PUSH
        # rrrrrrrr
        register = memory[pc + 1]
        # decrement the Stack Pointer (SP)
        registers[SP] -= 1
        # read the next value for register location
        register_value = registers[register]
        # take the value in that register and add to stack
        memory[registers[SP]] = register_value
        pc += 2
    elif command == POP:
        # POP Rrrrrrrr
        # POP value of stack at location SP
        value = memory[registers[SP]]
        register = memory[pc + 1]
        # store the value into register given
        registers[register] = value
        # increment the Stack Pointer (SP)
        registers[SP] += 1
        pc += 2

    else:
    # if command is non recognizable
        print(f"Unknown instruction {command}")
        sys.exit(1)
        # lets crash :(
    