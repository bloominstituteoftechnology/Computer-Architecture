import sys

# machine that excecutes an instruction

# op-code - represent the instruction that is supposed to be executed 
PRINT_HI = 1
HALT = 2
PRINT_NUM = 3
SAVE = 4 # SAVE a val in reg
PRINT_REGISTER = 5
ADD = 6 #takes 2 reg A and B, adds both and stores in reg A
PUSH = 7 # takes in a register and stores a val in that reg on top of a stack 
POP = 8  # takes in a register and stores topmost element in the stack in it.  

def load_memory():
    program = [
        PRINT_HI,
        SAVE, # save val 65 in reg 2 
        65,
        2,
        SAVE,
        20,
        3,
        PUSH,
        2,
        PUSH,
        3,
        POP,
        4,
        POP,
        0,
        HALT
    ]
    space_for_stack = 128 - len(program)
    memory = program + [0] * space_for_stack
    return memory

memory = load_memory()

registers = [0] * 8 #8 registers
stack_pointer_register = 7
registers[stack_pointer_register] = len(memory)-1 #address of stack pointer

program_counter = 0 # points to curr inst we need to execute next 
running = True 

#keep looping while not Halted

while running:
    command_to_execute = memory[program_counter]

    if command_to_execute == PRINT_HI:
        print("hi")
        program_counter+=1
    elif command_to_execute == PRINT_NUM:
        number_to_print = memory[program_counter +1]
        print(f"{number_to_print}")
        program_counter+=2
    elif command_to_execute == SAVE:
        value_to_save = memory[program_counter+1]
        register_to_save_it_in = memory[program_counter+2]
        registers[register_to_save_it_in] = value_to_save
        program_counter+=3
    elif command_to_execute == PRINT_REGISTER:
        register_to_print = memory[program_counter+1]
        print(f"{registers[register_to_print]}")
        program_counter +=2
    elif command_to_execute == ADD:
        register_a = memory[program_counter+1]
        register_b = memory[program_counter+2]
        sum_of_reg = registers[register_a]+registers[register_b]
        registers[register_a] = sum_of_reg
        program_counter +=3

    elif command_to_execute == HALT:
        running = False
        program_counter+=1
    elif command_to_execute == PUSH:
        registers[stack_pointer_register] -=1 # decrement stack pointer
        register_to_get_value_in  = memory[program_counter+1]
        value_in_register = registers[register_to_get_value_in]
        memory[registers[stack_pointer_register]] = value_in_register
        program_counter +=2
    elif command_to_execute == POP:
        register_to_pop_value_in = memory[program_counter+1]
        registers[register_to_pop_value_in] = memory[registers[stack_pointer_register]]
        registers[stack_pointer_register]+=1 
        program_counter+=2
    else:
        print("unknown instruction {command_to_execute}")
        sys.exit(1)

print (registers)
print (memory)




