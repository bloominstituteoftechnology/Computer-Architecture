"""computer emulator
software that pretends to be hardward
Turing complete-it can solve any problem for which there is an algorithn"""
import sys

#memory = [0]*256 #RAM
PRINT_THIS = 1
HALT = 2
SAVE_REG = 3 # run, ex, register[1]=37
PRINT_REG = 4 # run, ex, print(register[1])
ADD = 5

memory = [
    PRINT_THIS, 
    PRINT_THIS, 
    PRINT_THIS,
    SAVE_REG,  # SAVE R1 37
    1,  # REG address
    37, # value to save
    SAVE_REG,  # SAVE R1 37
    2,  
    3,
    PRINT_REG,  # print R1 <--PC
    1, 
    ADD, # add R1, R2, register[1]+register[2]
    1, 
    2,
    PRINT_REG,  # print R1 <--PC
    1,
    HALT,
    PRINT_THIS,
    ]

register = [0] * 8 # 8 general-purpose registers, like varibles, R0, R1, R2, ..., R7

pc = 0 # program counter, index of current instruction
running = True

while running:
    ir = memory[pc] # instruction register
    
    if ir == PRINT_THIS:
        print('hello')
        pc += 1

    elif ir == SAVE_REG: 
        # this is a three bit instrucition
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        register[reg_num] = value
        pc += 3

    elif ir == PRINT_REG:
        # this is a 2 bit instruction
        reg_num = memory[pc + 1]
        print(register[reg_num])
        pc += 2 

    elif ir == ADD:
        reg_num1 = memory[pc + 1]
        reg_num2 = memory[pc + 2]
        register[reg_num1] += register[reg_num2]
        pc += 3

    elif ir == HALT:
            running = False
            pc += 1
            
    else: 
        print(f"unknow instruction {ir} at address {pc}")
        sys.exit(1)
