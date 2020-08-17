PRINT_JENN = 0b0000001
HALT       = 0b0000010
PRINT_NUM  = 0b0000011 # command # 3
SAVE       = 0b0000100
PRINT_REGISTER = 0b0000101
ADD        = 0b10000110 # command #6
PUSH       = 0b01000111 # 1 operand, command #7
POP        = 0b01001000 # 1 operand, command #8
CALL       = 0B01011001
'''Rules of the game
1- We store everything in memory
2- we move our PC to step through memory and execute commands
'''
import sys
# memory = [
#     PRINT_JENN,
#     PRINT_JENN,
#     PRINT_NUM,
#     99,
#     SAVE,
#     42,
#     2,
#     PRINT_REGISTER,
#     2,
#     SAVE,
#     42,
#     3,
#     ADD,
#     2,
#     3,
#     PRINT_REGISTER,
#     2,
#     HALT
# ]
registers = [None] * 8
memory = [None] * 256
running = True
pc = 0

registers[7] = 0xF4

def load_program():
    address = 0
    try:
        with open(sys.argv[1]) as file:
            for line in file:
                comment_split = line.split('#')
                poss_num = comment_split[0]
                poss_num.strip()

                if poss_num == '':
                    continue
                if poss_num[0] == '1' or poss_num[0] == 0:
                    num = poss_num[:8]
                    print(f'{num}: {int(num, 2)}')
                    memory[address] = int(num, 2)
                    address += 1

    except FileNotFoundError:
        print(f'{sys.argv[0]}: {sys.argv[1]} not found')
load_program()
            
while running:
    
    command = memory[pc]
    num_operands = command >> 6
    
    if command == PRINT_JENN:
        print ("Jenn")
        pc += 1
        
    elif command == PRINT_NUM:
        num_to_print = memory[pc + 1]
        print (num_to_print)
        pc += 2
        
    elif command == SAVE:
        num =  memory[pc +1]
        index = memory[pc + 2]
        registers[index] = num
        
        pc += 3
        
    elif command == PRINT_REGISTER:
        reg_idx = memory[pc +1]
        print(registers[reg_idx])
        
        pc += 2
        
    elif command == ADD:
        first_reg_idx = memory[pc + 1]
        second_reg_idx = memory[pc + 2]
        registers[first_reg_idx] += registers[second_reg_idx]

    elif command == PUSH:
        registers[7] -= 1
        register_num = memory[pc + 1]
        num_to_push = registers[register_num]
        SP = registers[7]
        memory[SP] = num_to_push


    elif command == POP:
        SP = registers[7]
        popped_value = memory[SP]
        register_num = memory[pc + 1]
        registers[register_num] = popped_value
        registers[7] += 1

    elif command == HALT:
        running = False

    elif command == CALL:
        next_inst_add = pc + 2

        registers[7] -= 1

        SP = registers[7]

        memory[SP] = next_inst_add

        reg_address = memory[pc + 1]
        address_to_jump = registers[reg_address]
        pc = address_to_jump
    
    