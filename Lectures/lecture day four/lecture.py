import sys
# a machine that simply executes an instruction 

# op-code - they represent the instruction that is supposed to be executed
PRINT_HI = 1
HALT = 2
PRINT_NUM = 3
SAVE = 4 # save a value in a given register
PRINT_REGISTER = 5 # print value stored in register
ADD = 6 # TAKES IN TWO REGISTERS, a and b and adds both values contained in the registers and stores it in reg A
PUSH = 7 # takes in a register and stores the value in that register on top of the stack
POP = 8 # takes in a register and stores the topmost element in the stack in it
CALL = 9
RET = 10
PRINT_SUBROUTINE_INSTRUCTION = 11

def load_memory():
    PROGRAM = [
        PRINT_HI,
        SAVE,
        7,
        2,
        CALL,
        2,
        HALT,
        PRINT_SUBROUTINE_INSTRUCTION,
        SAVE,
        500,
        0,
        RET
    ]

    space_for_stack = 128 - len(PROGRAM)
    memory = PROGRAM + [0] * space_for_stack
    return memory

memory = load_memory()
program_counter = 0 # points to the current instruction we need to execute next
running = True
registers = [0] * 8
stack_pointer_register = 7 # register number that contains the address of the stack pointer
registers[stack_pointer_register] = len(memory) - 1


#keep loopiing while not halted.
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

    elif command_to_execute == PUSH:
        registers[stack_pointer_register] -= 1 # decrement stack pointer
        register_to_get_value_in = memory[program_counter + 1]
        value_in_register = registers[register_to_get_value_in]

        memory[registers[stack_pointer_register]] = value_in_register
        
        program_counter += 2

    elif command_to_execute == POP:
        register_top_pop_value_in = memory[program_counter + 1]
        registers[register_top_pop_value_in] = memory[registers[stack_pointer_register]]

        registers[stack_pointer_register] += 1

        program_counter += 2

    elif command_to_execute == CALL:
        # it stores the address of the next instruction on top of the stack
        registers[stack_pointer_register] -= 1
        address_of_next_instruction = program_counter + 2
        memory[registers[stack_pointer_register]] = address_of_next_instruction

        # it then jumps to the address stored in that register
        register_to_get_address_from = memory[program_counter + 1]
        program_counter = registers[register_to_get_address_from]

    elif command_to_execute == RET:
        # doesn't take in any operands, sets the program counter to the topmost element of the stack and pops it
        program_counter = memory[registers[stack_pointer_register]]
        registers[stack_pointer_register] += 1

    
    elif command_to_execute == PRINT_SUBROUTINE_INSTRUCTION:
        print("Hi I am in a subroutine!")
        program_counter += 1
    else:
        print(f"error: Uknown instruction {command_to_execute}")
        sys.exit(1)

print(f"Registers: {registers}")
print(f"Memory: {memory}")   