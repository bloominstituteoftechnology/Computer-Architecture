import sys
# a machine that simply executes an instruction 

# op-code - they represent the instruction that is supposed to be executed
PRINT_HI = 1
HALT = 2
PRINT_NUM = 3
SAVE = 4 # save a value in a given register
PRINT_REGISTER = 5 # print value stored in register
ADD = 6 # TAKES IN TWO REGISTERS, a and b and adds both values contained in the registers and stores it in reg A


memory = [
    PRINT_HI,
    SAVE, # Save 65 2 means save the value 65 in the register 2
    65,
    2,
    SAVE, # Save 20 3 means save the value 20 in the register 3
    20,
    3,
    ADD, # ADD 2 3 means add the values from register 2 and 3 and save them in 2
    2,
    3,
    PRINT_REGISTER, # Will print the value from register 2
    2,
    HALT
]

program_counter = 0 # points to the current instruction we need to execute next
running = True

registers = [0] * 8

# keep loopiing while not halted.
while running:
    command_to_execute = memory[program_counter]

    if command_to_execute == PRINT_HI:
        print("HI")
        program_counter += 1

    elif command_to_execute == PRINT_NUM:
        number_to_print = memory[program_counter + 1]
        print(f"{number_to_print}")
        program_counter += 2

    elif command_to_execute == HALT:
        running = False
        program_counter += 1

    elif command_to_execute == SAVE:
        value_to_save = memory[program_counter + 1]
        register_saving_to = memory[program_counter + 2]
        registers[register_saving_to] = value_to_save
        program_counter += 3

    elif command_to_execute == PRINT_REGISTER:
        register_to_print = memory[program_counter + 1]
        print(f"{registers[register_to_print]}")
        program_counter += 2

    elif command_to_execute == ADD:
        # 2 registers
        register_a = memory[program_counter + 1]
        register_b = memory[program_counter + 2]

        # 2 values 
        register_a_value = registers[register_a]
        register_b_value = registers[register_b]

        registers[register_a] = register_a_value + register_b_value
        program_counter += 3

    else:
        print(f"error: Uknown instruction {command_to_execute}")
        sys.exit(1)

    