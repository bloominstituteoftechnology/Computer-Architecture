'''Simple Byte machine for emulating a CPU'''
import sys

PRINT_GWEN       = 0b00000001
HALT             = 0b00000010
PRINT_NUM        = 0b00000011
SAVE             = 0b00000100
ADD              = 0b10000110
PRINT_REGISTER   = 0b00000101
PUSH             = 0b01000111 #1 operand, command 7
POP              = 0b01001000 #1 operand, command 8

memory = [0]*256 #emulated RAM
#While loop for stepping through memory
def load_program():
    address = 0
    try:
        with open(sys.argv[1]) as file:
            for line in file:
                comment_split = line.split('#')
                possible_num = comment_split[0]
                if possible_num == '':
                    continue
                if possible_num[0] == '1' or possible_num[0] == '0':
                    num = possible_num[:8]
                    memory[address] = int(num,2)
                    address+=1
    except FileNotFoundError:
        print(f'{sys.argv[0]}: {sys.argv[1]} not found!')

load_program()


running = True
pc = 0

#What arguments does SAVE need to
#save the number to register 2
# Registers use as variables
# R0-R7 These would be physically with cpu
registers = [None]*8
registers[7] = 0xF4

while running:
    '''I chose to make sure not to use variable names
    inside this logic, just to make sure I understood it
    
    memory[pc] is current command
    memory[pc+1] in PRINT_NUM and SAVE will be an interger used by command
    memory[pc+2] in SAVE will be a register to save variables to
    memory[pc+1] in PRINT_REGISTER is register index to be printed'''
    if memory[pc] == PRINT_GWEN:
        print("Gwen!")
        pc+=1

    elif memory[pc] == PRINT_NUM:
        print(memory[pc+1])
        pc+=2

    elif memory[pc] == SAVE:
        registers[memory[pc+2]] = memory[pc+1]
        print(f'Saved {memory[pc+1]}')
        pc+=3

    elif memory[pc] == ADD:
        registers[memory[pc+1]] = registers[memory[pc+1]] + registers[memory[pc+2]]
        print(f'Memory register {memory[pc+1]} is now {registers[memory[pc+1]]}')
        pc+=3

    elif memory[pc] == PRINT_REGISTER:
        print(registers[memory[pc+1]])
        pc+=2
    
    elif memory[pc] == PUSH:
        #decrement the pointer
        registers[7]-=1
        #copy value from given register, and put it into stack
        value = registers[memory[pc+1]]
        address =  registers[7]
        memory[address] = value
        pc+=2

    elif memory[pc] == POP:
        #copy value from top of stack
        value = memory[registers[7]]
        #put it into given register
        registers[memory[pc+1]] = value
        #increment stack pointer
        registers[7]+=1
        pc+=2


    
    elif memory[pc] == HALT:
        print('Halting!')
        running = False



