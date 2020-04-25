import sys
​
PRINT_TIM   =    1
HALT        =    2
PRINT_NUM   =    3
SAVE        =    4
PRINT_REGISTER = 5
ADD           =  6
​
memory = [
    PRINT_TIM,
    PRINT_TIM,
    PRINT_TIM,
    PRINT_NUM,
    14,
    SAVE,
    99,
    2,
    SAVE,
    101,
    1,
    ADD,
    1,
    2,
    PRINT_REGISTER,
    1,
    HALT
]
​
running = True
pc = 0
​
registers = [0] * 8 # [0, 0, 0, 0, 0, 0, 0, 0]
​
while running is True:
    command = memory[pc]
​
    if command == PRINT_TIM:
        print("Tim!")
        pc += 1
​
    elif command == PRINT_NUM:
        print(memory[pc + 1])
        pc += 2
​
    elif command == SAVE:
        reg_index = memory[pc + 2]
        number_to_save = memory[pc + 1]
        registers[reg_index] = number_to_save
        pc += 3
​
    elif command == PRINT_REGISTER:
        reg_index = memory[pc + 1]
        print(registers[reg_index])
​
        pc += 2
​
    elif command == ADD:
     # reg1 = reg1 + reg2
        reg_1 = memory[pc + 1]
        reg_2 = memory[pc + 2]
        registers[reg_1] = registers[reg_1] + registers[reg_2]
​
        pc += 3
​
    elif command == HALT:
        running = False
​
    else:
        print("Error!")
        sys.exit(1)