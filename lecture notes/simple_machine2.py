import sys

PRINT_TIM = 0b00000001
HALT      = 0b00000010
PRINT_NUM = 0b01000011  # a 2-byte command, takes 1 argument
SAVE      = 0b10000100  # a 3-byte command, takes 2 arguments
PRINT_REG = 0b01000101
ADD       = 0b10100110 

# a data-driven machine
# function call
# a "variable" == registers for our programs to save things into


# RAM
memory = [0] * 256

# registers, R0-R7
registers = [0] * 8

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

    elif command == HALT:
        running = False

    number_of_operands = command >> 6
    pc += (1 + number_of_operands)
    # pc += 1  # so we don't get sucked into an infinite loop!

'''
In terminal run:
    python simple_machine2.py our_program.ls8
'''