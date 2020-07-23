PRINT_TIM   = 0b01  # 1  This is 1-byte command
HALT        = 0b10  # 2
PRINT_NUM   = 0b11  # opcode 3
SAVE        = 0b100
PRINT_REG   = 0b101 # opcode 5
ADD         = 0b110
PUSH        = 0b111
POP         = 0b1000
CALL        = 0b1001
RET         = 0b1010



# RAM (a slot in memory)
# memory = [
#     PRINT_TIM,
#     PRINT_TIM,
#     PRINT_NUM,  # this is 2-byte command, because we want to print the next thing (42)
#     42,
#     SAVE,       # this is a 3-byte instruction, because it takes next 2 additional bytes
#     2,          # register to put number in
#     99,         # number to save
#     SAVE,
#     3,
#     1,
#     ADD,        # registers[2] = registers[2] + registers[3]
#     2,
#     3,
#     PRINT_REG,  # prints whatever is on specified register
#     2,          # register we want to look at
#     HALT
# ]     

import sys

memory = [0] * 256

def load_memory(file_name):
    try:
        address = 0
        with open(file_name) as file:
            for line in file:
                split_line = line.split('#')[0]
                command = split_line.strip()
                
                if command == '':
                    continue

                instruction = int(command, 2)
                memory[address] = instruction
                
                address += 1
                

    except FileNotFoundError:
        print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
        sys.exit()

if len(sys.argv) < 2:
    print("Please pass in a second filename: python in_and_out.py second_filename.py")
    sys.exit()

file_name = sys.argv[1]
load_memory(file_name)

# Write a program to pull each command out of memory and execute
# we can loop over it!

# register aka memory
registers = [0] * 8
registers[7] = 0xF4
# [0,0,99,0,0,0,0,0]
# save the number 99 into R2 (register2)
# registers ranges: R0-R7


pc = 0 # program counter
running = True
while running:
    command = memory[pc]
    
    if command == PRINT_TIM:
        print("Tim!")
        pc += 1
    
    if command == HALT:
        running = False
        pc += 1
    
    if command == PRINT_NUM:
        num_to_print = memory[pc+1]
        print(num_to_print)
        pc += 2

    if command == SAVE:
        reg = memory[pc + 1]
        num_to_save = memory[pc + 2]
        registers[reg] = num_to_save
        pc += 3

    if command == PRINT_REG:
        reg_index = memory[pc+1]
        print(registers[reg_index])
        pc += 2
    
    if command == ADD:
        first_reg = memory[pc+1]
        sec_reg = memory[pc+2]
        registers[first_reg] = registers[first_reg] + registers[sec_reg]
        pc += 3

    if command == PUSH:
        # decrement the stack pointer
        registers[7] -= 1

        # get a value from the given register
        reg = memory[pc+1]
        value = registers[reg]
        
        # put it on the stack pointer address
        sp = registers[7]
        memory[sp] = value

        pc += 2

    if command == POP:
        # get the stack pointer (where do we look?)
        sp = registers[7]

        # get register number to put value in
        reg = memory[pc+1]
        
        # use stack pointer to get the value
        value = memory[sp]
        # put the value into the given register
        registers[reg] = value

        # increment our stack pointer
        registers[7] += 1
        # increment our program counter
        pc += 2

    if command == CALL:
        # get register number
        reg = memory[pc+1]
        # get the address to jump to, from the register
        address = registers[reg]

        # push command right after CALL onto the stack
        return_address = pc + 2
        # decrement stack pointer
        registers[7] -= 1
        sp = registers[7]
        # put return_address on the stack
        memory[sp] = return_address
        
        # then look at register, jump to that address
        pc = address

    if command == RET:
        # pop the return address off the stack
        sp = registers[7]
        return_address = memory[sp]
        registers[7] += 1

        # go to return address: set the pc to return address
        pc = return_address
