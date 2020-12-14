import sys

PRINT_TIM = 0b00000001
HALT      = 0b00000010
PRINT_NUM = 0b01000011  # a 2-byte command, takes 1 argument
SAVE      = 0b10000100  # a 3-byte command, takes 2 arguments
PRINT_REG = 0b01000101
ADD       = 0b10100110
PUSH      = 0b01000111
POP       = 0b01001000


# a data-driven machine
# function call
# a "variable" == registers for our programs to save things into


# RAM
memory = [0] * 256

# registers, R0-R7
registers = [0] * 8

# set the stack pointer
registers[7] = 0xF4

running = True

# program counter
pc = 0

def load_ram():
    try:
        if len(sys.argv) < 2:
            print(f'Error from {sys.argv[0]}: missing filename argument')
            print(f'Usage: python3 {sys.argv[0]} <somefilename>')
            sys.exit(1)


        # add a counter that adds to memory at that index
        ram_index = 0

        with open(sys.argv[1]) as f:
           for line in f:
                split_line = line.split("#")[0]
                stripped_split_line = split_line.strip()

                if stripped_split_line != "":
                    command = int(stripped_split_line, 2)
                    
                    # load command into memory
                    memory[ram_index] = command

                    ram_index += 1

    except FileNotFoundError:
        print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
        print("(Did you double check the file name?)")

load_ram()

while running:
    command = memory[pc]


    if command == PRINT_TIM:
        print('tim!')

    elif command == PRINT_NUM:
        num_to_print = memory[pc + 1]  # we already incremented PC!
        print(num_to_print)

        # pc += 1   # but increment again


    elif command == SAVE:
        num_to_save = memory[pc + 1]
        register_address = memory[pc + 2]

        registers[register_address] = num_to_save

        # shorter: 
        # registers[memory + 2] = memory[pc + 1]

        # pc += 2

    elif command == PRINT_REG:
        reg_address = memory[pc + 1]

        saved_number = registers[reg_address]

        print(saved_number)

        # print(registers[memory[pc + 1]])

    elif command == ADD:
        reg1_address = memory[pc + 1]
        reg2_address = memory[pc + 2]

        registers[reg1_address] += registers[reg2_address]

    elif command == PUSH:
        # decrement the SP
        ## at start, the SP points to address F4
        ### can just do arithmetic on hex, like F4 - 1
        ## R7 is our SP, currently points to (aka holds) F4
        registers[7] -= 1

        # copy value from given register into address pointed to by SP
        ##  value from register?
        register_address = memory[pc + 1]
        value = registers[register_address]

        ## copy into SP address
        ### now let's copy this value into our memory
        ### but where in memory???

        # memory[SP] = value
        # memory[register[7]] = value

        SP = registers[7]
        memory[SP] = value


    elif command == POP:
        # Copy the value from the address pointed to by `SP` to the given register.
        ## get the SP
        SP = registers[7]
        ## copy the value from memory at that SP address
        value = memory[SP]

        ## get the target register address
        ### aka, where should we put this value from RAM?
        register_address = memory[pc + 1]

        ## Put the value in that register
        registers[register_address] = value

        # Increment the SP (move it back up)
        registers[7] += 1


    elif command == HALT:
        running = False

    number_of_operands = command >> 6
    pc += (1 + number_of_operands)
    # pc += 1  # so we don't get sucked into an infinite loop!