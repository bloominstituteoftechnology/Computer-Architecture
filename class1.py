PRINT_TIM = 0b00000001
HALT      = 0b00000010
PRINT_NUM = 0b00000011
SAVE      = 0b00000100
PRINT_REG = 0b00000101
ADD       = 0b00000111
memory = [
    
    PRINT_TIM,
     
    PRINT_NUM,
    42,
    PRINT_NUM,
    SAVE,
    2,
    3,
    ADD,
    PRINT_REG,
    2,
    HALT
]


registers = [0]*8
pc =0
running = True

while running:
    command = memory[pc]
  
    if command == PRINT_TIM:
        print('Tim')
    elif command == PRINT_NUM:
        pc+=1
        number = memory[pc]
        print(number)  
    
    elif command == ADD:
        #pullout Args
        reg_idx_1 = memory[pc +1]    
        reg_idx_2 = memory[pc +2]
    elif command == SAVE:
        #getout the args
        reg_idx = memory[pc+1]
        value = memory[pc+2]
        registers[reg_idx]=value
        #increment program counter
        pc +=2
    elif command == PRINT_REG:
        #get out arg
        reg_idx = memory[pc+1]
        #arg is a pointer to a register
        value = registers[reg_idx]
        print(value) 
        pc +=2     
    elif command == HALT:
        running == False
    else:
        print('unknown command')    
        running:False
    pc +=1    