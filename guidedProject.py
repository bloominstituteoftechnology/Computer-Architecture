PRINT_TIM = 0b00000001
HALT = 0b00000010
PRINT_NUM = 0b00000011
SAVE = 0b00000100
PRINT_REGISTER = 0b00000101
ADD = 0b00000110

# SAVE into R2, the number 99
memory = [
    PRINT_TIM,
    PRINT_NUM, 
    42,      
    SAVE,
    2,       # into R2
    10,
    SAVE,
    3,       # into R2
    10,
    ADD,    # registers[2] = registers[2] + registers[3]
    2,
    3,
    PRINT_REGISTER,
    2,
    HALT
          ]


# cabinets in your shop: registers
# storage unit: cache
# warehouse outside town: RAM

# registers
# physically located on CPU, treat as variables

# R0-R7
registers = [0] * 8

# cpu should now step through memory and take actions based on commands it finds

# a data-driven machine

# program counter, a pointer
pc = 0
running = True

while running:
    command = memory[pc]

    if command == PRINT_TIM:
        print("tim!")

    elif command == PRINT_NUM:
        # number = memory[pc + 1]
        pc += 1
        number = memory[pc]
        print(number)

    elif command == SAVE:
        # get out the arguments
        # pc+1 is reg idx, pc+2 value
        reg_idx = memory[pc + 1]
        value = memory[pc + 2]

        # put the value into the correct register
        registers[reg_idx] = value

        # increment program counter by 2
        ## 2 + 1 below == 3-byte command
        pc += 2

    elif command == PRINT_REGISTER:
        # get out the argument
        reg_idx = memory[pc + 1]

        # the argument is a pointer to a register
        value = registers[reg_idx]
        print(value)

        # increment program counter
        pc += 1

    elif command == ADD:
        # pull out the arguments
       reg_idx_1 = memory[pc + 1] 
       reg_idx_2 = memory[pc + 2] 

        # add regs together
       registers[reg_idx_1] = registers[reg_idx_1] + registers[reg_idx_2]

       # increment program counter
       pc += 2


    elif command == HALT:
        running = False

    else:
        print('unknown command!')
        running = False

    pc += 1
