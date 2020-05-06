import sys

# op codes, this is what you would give a programmer as "documentation"
PRINT_ARTEM    = 1
HALT           = 2
PRINT_NUM      = 3
SAVE           = 4
PRINT_REGISTER = 5
ADD            = 6

# sample program that prints artems
print_artem_program = [
    PRINT_ARTEM,
    PRINT_ARTEM,
    PRINT_ARTEM,
    PRINT_ARTEM,
    HALT,
]

# sample program that prints some numbers
print_some_nums = [
    PRINT_NUM,
    15,
    PRINT_NUM,
    15,
    PRINT_NUM,
    37,
    PRINT_ARTEM,
    HALT
]

# sample program that saves and prints numbers from registers
save_num_to_reg = [
    SAVE, # SAVE, VAL, REG_NUM
    65, 
    2,
    PRINT_REGISTER,
    2,
    SAVE, # SAVE, VAL, REG_NUM
    14568292, 
    6,
    PRINT_REGISTER,
    2,
    PRINT_REGISTER,
    6,
    HALT
]

# sample program that adds to register values together
add_numbers = [
    SAVE, # SAVE number 12 to reg 1
    12,
    1,
    SAVE, # SAVE number 45 to reg 2
    45,
    2,
    ADD, # Reg1 += Reg2  (we add the two values in the two registers, and store the result in the first register)
    1,
    2,
    PRINT_REGISTER,
    1,
    SAVE,
    10,
    2,
    ADD,
    1,
    2,
    PRINT_REGISTER,
    1,
    HALT,
]

# this is where we "load" a program
memory = add_numbers



# ALL THE CODE BELOW IS THE "COMPUTER"
running = True
pc = 0
registers = [0] * 8

while running:
    # lets receive some instructions, and execute them
    command = memory[pc]

    # if command is PRINT_ARTEM
    if command == PRINT_ARTEM:
        # print out artem's name
        print('Artem!')
        pc += 1

    # if command is HALT
    elif command == HALT:
        running = False
        pc += 1
        # shutdown

    elif command == PRINT_NUM:
        # look at the next line in memory
        # print the number thats in that spot
        num = memory[pc + 1]
        print(num)
        pc += 2

    elif command == SAVE:
        # we expect to see two numbers after the instruction
        # number to save, and register location
        num_to_save = memory[pc + 1]
        register = memory[pc + 2]
        registers[register] = num_to_save
        pc += 3
    
    elif command == PRINT_REGISTER:
        # we expect to see one number after the instruction
        # number of register location
        register = memory[pc + 1]
        print(registers[register])
        pc += 2
    
    elif command == ADD:
        # we expect to see two numbers after the instruction
        # both register locations
        # we will save the result into the first register given to us
        register1 = memory[pc + 1]
        register2 = memory[pc + 2]
        val1 = registers[register1]
        val2 = registers[register2]
        registers[register1] = val1 + val2
        pc += 3
    else:
    # if command is non recognizable
        print(f"Unknown instruction {command}")
        sys.exit(1)
        # lets crash :(
    