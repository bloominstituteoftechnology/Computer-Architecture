PRINT_ME    =   0b00000001
STOP        =   0b00000010
PRINT_NUM   =   0b00000011
SAVE        =   0b00000100
PRINT_REG   =   0b00000101

memory = [
    PRINT_ME,
    PRINT_ME,
    PRINT_ME,
    PRINT_NUM,
    99,
    SAVE, 
    42,
    2,
    PRINT_REG,
    2,
    STOP,
    ]


running = True
pc = 0

# We want to save the number 42 to register R2

# registers (use as variables)
# R0-R7
registers = [None] * 8

# while loop to make machine run 'continuously'
while running:
    
    command = memory[pc]

    if command == PRINT_ME:
        print("Raul Jr!")

        pc += 1
    
    if command == PRINT_NUM:
        num_to_print = memory[pc + 1]
        print(num_to_print)
        pc += 2

    if command == SAVE:
        num_to_save = memory[pc +1]
        reg_index = memory[pc + 2]
        registers[reg_index] = num_to_save
        pc += 3
        print(num_to_save)
    
    if command == PRINT_REG:
        reg_to_print = memory[pc + 1]
        print(registers[reg_to_print])
        pc += 2

    if command == STOP:
        running = False
