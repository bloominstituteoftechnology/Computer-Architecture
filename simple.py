PRINT_JENN = 0b0000001
HALT       = 0b0000010
PRINT_NUM  = 0b0000011 # command # 3
SAVE       = 0b0000100
PRINT_REGISTER = 0b0000101

'''Rules of the game
1- We store everything in memory
2- we move our PC to step through memory and execute commands
'''

memory = [
    PRINT_JENN,
    PRINT_JENN,
    PRINT_NUM,
    99,
    SAVE,
    42,
    2,
    PRINT_REGISTER,
    2,
    HALT
]

running = True
pc = 0

registers = [None] * 8


while running:
    
    command = memory[pc]
    
    if command == PRINT_JENN:
        print ("Jenn")
        pc += 1
        
    if command == PRINT_NUM:
        num_to_print = memory[pc + 1]
        print (num_to_print)
        pc += 2
        
    if command == SAVE:
        num =  memory[pc +1]
        index = memory[pc + 2]
        registers[index] = num
        
        pc += 3
        
    if command == PRINT_REGISTER:
        reg_idx = memory[pc +1]
        print(registers[reg_idx])
        
        pc += 2
        
        
    if command == HALT:
        running = False
    
    