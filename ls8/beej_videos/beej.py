'''
CPU
    executes instructions
    gets them out of RAM
    Registers(like variables)
        fixed names R0-R7
        fixed number of registers/variabes -- 8 of them
        fixed size -- 8 bits

Memory(RAM)
    A big array of bytes 1 byte = 8 bits
        0b00000000 == decimal 0
        0b11111111 == decimal 255
    each memory slot has an index, and a value stores at that index
    That index into memory AKA
        pointer
        location
        address

Operands are the arguements to the instructions
Opcode is the name of the instruction
'''
import sys

#parse the command line
program_filename = sys.argv[0]

#MEMORY ARRAY
# memory = [
#     #ALL ITEMS IN MEMORY ARE NUMBERS
#     1, #PRINT JENN
#     3, #SAVE_REG R2, 99 register to save in, the value being saved
#     2, # R2
#     99,#  value 99
#     4, #PRINT_REG R2
#     2, # print register 2
#     2, #HALT
# ]

memory = [0] * 256 # creates empty memory
register = [0] * 8 #creates a list of 8 0's

#-- Load Program --
address = 0
with open(program_filename) as f:  
    for line in f:
        line = line.split('#')
        line = line[0].strip()

        if line == '':
            continue

        memory[address] = int(line, 2) # converts to base 2

        address += 1
#-- Run Loop --


pc = 0 #Program Counter, index into memory of the current instruction
       #AKA a pointer to the current instruction
sp = 7
register[sp] = 0xf4 # Stack pointer (SP)

running = True       

#CPU
while running:
    inst = memory[pc]

    if inst == 1:
        print("Jenn")
        pc += 1
        
    elif inst == 2: # In project -> HLT
        running = False
        
    elif inst == 3: #save reg -> In project - LDI
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        register[reg_num] = value
        pc += 3

    elif inst == 4: # in project -> PRN
        reg_num = memory[pc + 1]
        print (register[reg_num])
        pc += 2

    elif inst == 5: # PUSH
        #decrement stack pointer
        register[sp] -= 1
        register[sp] &= 0xff # keeps the register in rangeS
        #get register value
        reg_num = memory[pc + 1]
        value = register[reg_num]
        #store in memory
        address_to_push_to = register[sp]
        memory[address_to_push_to] = value
        pc += 2

    elif inst == 6: # POP
        #get value from RAM
        address_to_pop_from = register[sp]
        value = memory[address_to_pop_from]
        #store in the given register
        reg_num = memory[pc + 1]
        register[reg_num] = value
        #increment the stack pointer
        register[sp] += 1

        pc += 2

    else:
        print(f"Unknown instruction {inst}")


