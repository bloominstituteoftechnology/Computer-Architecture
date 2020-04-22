import sys
# stack is last in first out
'''
PUSH:
    1. decrement SP
    2. copy value from reg into memory at SP

POP:
    1. copy the value from memory into reg
    2. Increment SP
'''
# write program in python that runs programs:
program_filename = sys.argv[0]
print(program_filename)
sys.exit()
#print beej = 1 
# halt = 2

PRINT_BEEJ = 1
HALT  = 2
PUSH =5
POP = 6 

'''
memory = [
    PRINT_BEEJ,
    PRINT_BEEJ,
    PRINT_BEEJ,
    HALT
]
'''
memory = [0] * 256
register = [0] * 8


address = 0
with open('beej.ls8') as f:
    for line in f:
        line = line.split('#')
        line = line[0].strip()
        if line == '':
            continue
        try:
            line = int(line)
        except ValueError:
            continue
        memory[address] = int(line)
        address += 1
        print(line)

sys.exit()
# address of the current instruction
# which slot in memory it is
pc = 0
running = True
while running:
    instruction = memory[pc]
    if instruction == PRINT_BEEJ:
        print("beej!")
        # next instruction
        pc += 1
    elif instruction == HALT:
        running = False

# another form of storage is called register
# named like this R0 through R7
# they hold values and numbers
# this is fixed depending on the actual CPU
register = [0] * 8
# store value to register and print it out
SAVE_REG = 3
PRINT_REG = 4


# memory = [
#     PRINT_BEEJ,
#     SAVE_REG, # save the val 37 to R0
#     0, # represents Register 0 (operands)
#     37, # represents the value (operands)
#     PRINT_BEEJ,
#     PRINT_REG, # print R 0
#     0,
#     HALT
# ]
memory = [0] * 256
register = [0] * 8
with open(program_filename) as f:
    for line in f:
        print(line)

sys.exit()
# address of the current instruction
# which slot in memory it is
pc = 0
running = True
while running:
    instruction = memory[pc]


    if instruction == PRINT_BEEJ:
        print("beej!")
        # next instruction
        pc += 1
    # add instruction
    elif instruction == SAVE_REG:
        register_num = memory[pc + 1]
        value = memory[pc + 2]
        register[0] = 37
        pc += 3
    elif instruction == PRINT_REG:
        register_num = memory[pc + 1]
        value = register[register_num]
        print(value)
        pc += 2
    elif instruction == HALT:
        running = False
    else:
        print("Unknown Instruction")

