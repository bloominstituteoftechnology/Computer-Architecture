import sys
​
PRINT_TIM = 0b00000001
HALT = 0b00000010
PRINT_NUM = 0b01000011  # a 2-byte command, takes 1 argument
SAVE = 0b10000100  # a 3-byte command, takes 2 arguments
PRINT_REG = 0b01000101
ADD = 0b10100110
PUSH = 0b0100111
POP = 0b01001000
​
​
# a data-driven machine
# function call
# a "variable" == registers for our programs to save things into
​
​
# RAM
memory = [0] * 256
​
# registers, R0-R7
registers = [0] * 8
registers[7]
= 0xF4​
running = True
​
# program counter
pc = 0
​


def load_ram():
    try:
        if len(sys.argv) < 2:
            print(f'Error from {sys.argv[0]}: missing filename argument')
            print(f'Usage: python3 {sys.argv[0]} <somefilename>')
            sys.exit(1)


​
​
# add a counter that adds to memory at that index
ram_index = 0
​
with open(sys.argv[1]) as f:
    for line in f:
        split_line = line.split("#")[0]
        stripped_split_line = split_line.strip()
​
if stripped_split_line != "":
    command = int(stripped_split_line, 2)

    # load command into memory
    memory[ram_index] = command
​
ram_index += 1
​
except FileNotFoundError:
    print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
    print("(Did you double check the file name?)")
​
load_ram()
​
while running:
    command = memory[pc]
​
​
if command == PRINT_TIM:
    print('tim!')
​
elif command == PRINT_NUM:
    num_to_print = memory[pc + 1]  # we already incremented PC!
    print(num_to_print)
​
# pc += 1   # but increment again
​
​
elif command == SAVE:
    num_to_save = memory[pc + 1]
    register_address = memory[pc + 2]
​
registers[register_address] = num_to_save
​
# shorter:
# registers[memory + 2] = memory[pc + 1]
​
# pc += 2
​
elif command == PRINT_REG:
    reg_address = memory[pc + 1]
​
saved_number = registers[reg_address]
​
print(saved_number)
​
# print(registers[memory[pc + 1]])
​
elif command == ADD:
    reg1_address = memory[pc + 1]
    reg2_address = memory[pc + 2]
​
registers[reg1_address] += registers[reg2_address]
​
elif command == HALT:
    running = False

elif command == PUSH
# decrement the stack pointer
# at address f4
# can just do arithmetic, F4 - 1
# R7 is our sp, has value f4
registers[7] -= 1

# copy value from given register into address pointed to by SP
# value from register
register_address = memory[pc+1]
value = registers[register_address]

# copy into sp address
# copy this value into memory,
# put it where stack pointer wants us to put it.
SP = register[7]
memory[SP] = value

elif command = "POP":
    # copy value from address pointed to sp to the given register
    # get stack pointer and get value from memory at sp address
    SP = registers[7]
    value = memory[SP]

    # get register address
    # aka where should we put this value from ram
    register_address = memory[pc+1]

    # put value in that register
    register[register_address] = value

    # increment the stack pointer
    registers[7] += 1


​
number_of_operands = command >> 6
pc += (1 + number_of_operands)
# pc += 1  # so we don't get sucked into an infinite loop!


# 01000111
# 00000010 #from r2


# making call and return

CALL = 0b01001001
RET = 0b00001010


def call(self):
    # step 1:push the return address onto the stack
    # find the address/index of the command AFTER Call
    next_command_address = pc + 2

    # push the address onto the stack
    # decrement the stack pointer
    reg[7] -= 1
    # put the next command address at the location in memory where the stack pointer points
    SP = reg[7]
    memory[SP] = next_command_address

    # step 2, jump, set the PC to wherever the registeer says
    # find the number of the register to look at
    register_num_jump = memory[pc+1]

    # get address of the subroutine out fo that register
    address_to_jump_to = registers[register_num_jump]

    # set the pc
    pc = address_to_jump_to

    elif command == RET:
        # pop the value from the top of the stack and store it in the pc

        # pop from the top of the stack
        # get the value first
        SP = registers[7]
        return_address = memory[SP]

        # then move the stack pointer up
        registers[7] += 1

    # step 2, jump back, set the pc to this value
    pc = return_address
