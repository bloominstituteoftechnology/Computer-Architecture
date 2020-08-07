PRINT_TIM      =  0b00000001
HALT           =  0b00000010
PRINT_NUM      =  0b00000011  # command 3
SAVE           =  0b00000100
PRINT_REGISTER =  0b00000101
​
#ADD
​
# Rules of our game
## we store everything in memory
## we move our PC to step through memory, and execute commands
​
memory = [
    PRINT_TIM, 
    PRINT_TIM,
    PRINT_NUM,
    99,
    SAVE, 
    42,  # number to save
    2,   # register to save into
    PRINT_REGISTER,
    2,
    HALT,       # <--- PC
          ]
​
running = True
pc = 0
​
# save the number 42 into R2
# what arguments does SAVE require?
​
# registers (use as variables)
# R0-R7
registers = [None] * 8
​
while running:
​
    command = memory[pc]
​
    if command == PRINT_TIM:
        print("Tim!")
​
        pc += 1
    
    if command == PRINT_NUM:
        number_to_print = memory[pc + 1]
        print(number_to_print)
​
        pc += 2
​
    if command == SAVE:
        num = memory[pc + 1]
        index = memory[pc + 2]
        registers[index] = num
​
        pc += 3
​
    if command == PRINT_REGISTER:
        reg_idx = memory[pc + 1]
        print(registers[reg_idx])
​
        pc += 2 
​
    if command == HALT:
        running = False