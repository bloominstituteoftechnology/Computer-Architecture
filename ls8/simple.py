PRINT_TIM = 0b0000001
HALT = 0b0000010

memory = [PRINT_TIM, PRINT_TIM, HALT]

running = True
pc = 0
  
while running:
    command = memory[pc]
    
    if command == PRINT_TIM:
        print('Tim!')
        
    if command == HALT:
        running = False
        
    pc += 1