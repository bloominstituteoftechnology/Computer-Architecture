PRINT_TIM      =  0b00000001
HALT           =  0b00000010
PRINT_NUM      =  0b01000011  # command 3
SAVE           =  0b10000100
PRINT_REGISTER =  0b01000101
ADD            =  0b10000110  # command 6
PUSH           =  0b01000111  # 1 operand, command 7
POP            =  0b01001000  # 1 operand, command 8
​
​
# Rules of our  game
## we store everything in memory
## we move our PC to step through memory, and execute commands
import sys
​
​
memory = [None] * 256
​
running = True
pc = 0
​
def load_program():
    address = 0
    try:
        with open(sys.argv[1]) as file:
            for line in file:
                comment_split = line.split('#')
​
                possible_num = comment_split[0]
​
                possible_num.strip()
​
                if possible_num == '':
                    continue
​
                if possible_num[0] == '1' or possible_num[0] == '0':
                    num = possible_num[:8]
​
                    print(f'{num}: {int(num, 2)}')
​
                    memory[address] = int(num, 2)
                    address += 1
​
    except FileNotFoundError:
        print(f'{sys.argv[0]}: {sys.argv[1]} not found')
​
load_program()
​
​
# Memory bus
## a bunch of wires that the CPU uses to send an address to RAM
## also a data bus: CPU sends data to RAM, RAM sends data to CPU
##     CPU
##  ||||||||
##  ||||||||
##  ||||||||
##     RAM
​
# 0b00000001
# 0b00000010
# 0b11111111
​
# registers (use as variables)
# R0-R7
registers = [None] * 8
registers[7] = 0xF4
​
while running:
​
    command = memory[pc]
​
    num_operands = command >> 6
​
    if command == PRINT_TIM:
        print("Tim!")
​
    elif command == PRINT_NUM:
        number_to_print = memory[pc + 1]
        print(number_to_print)
​
    elif command == SAVE:
        num = memory[pc + 1]
        index = memory[pc + 2]
        registers[index] = num
​
    elif command == PRINT_REGISTER:
        reg_idx = memory[pc + 1]
        print(registers[reg_idx])
​
    elif command == ADD:
        first_reg_idx = memory[pc + 1]
        second_reg_idx = memory[pc + 2]
​
        registers[first_reg_idx] += registers[second_reg_idx]
​
    elif command == PUSH:
        # decrement the pointer
        registers[7] -= 1
        # look ahead in memory to get the register number
        register_number = memory[pc + 1]
        # get value from register
        number_to_push = registers[register_number]
        # copy into stack
        SP = registers[7]
        memory[SP] = number_to_push
​
    elif command == POP:
        # use the SP as is
        SP = registers[7]
​
        # get value from last position of SP
        popped_value = memory[SP]
​
        # get register number
        # self.ram[pc + 1]
        register_number = memory[pc + 1]
        # copy into a register
        registers[register_number] = popped_value
​
        # move pointer, increment SP
        registers[7] += 1
​
​
​
    elif command == HALT:
        running = False
​
    # what if we set the pc directly?
    pc += num_operands + 1