import sys
PRINT_MACK = 1
HALT = 2
SAVE_REG = 3 # save a value in a register
PRINT_REG = 4 

memory = [
    PRINT_MACK, 
    PRINT_MACK,
    SAVE_REG, # SAVE_REG R0, 12. How do we do this?
    0,
    37, 
    PRINT_REG,
    0,
    PRINT_MACK,
    HALT 
]

registers = [0,0,0,0,0,0,0,0] # named r0-r7

halted = False

pc = 0 # "Program Counter": Index into the memory array AKA a pointer, address, location

while not halted:
    instruction = memory[pc]

    if instruction == PRINT_MACK:
        print("Mack!")
        pc += 1

    elif instruction == SAVE_REG:
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        registers[reg_num] = value 
        pc += 3
    elif instruction == PRINT_REG:
        reg_num = memory[pc + 1]
        print(registers[reg_num])
        pc += 2
    elif instruction == HALT:
        halted = True
    else:
        print(f'Unknown instruction: {instruction} at address {pc}')
        sys.exit(1)
