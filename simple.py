'''Simple Byte machine for emulating a CPU'''
PRINT_GWEN       = 0b00000001
HALT             = 0b00000010
PRINT_NUM        = 0b00000011
SAVE             = 0b00000100
PRINT_REGISTER   = 0b00000101

memory = [PRINT_GWEN,
          PRINT_GWEN,
          PRINT_NUM,
          99,
          SAVE,
          42,
          2,
          PRINT_REGISTER,
          2,
          HALT,
          ] #emulated RAM
#While loop for stepping through memory

running = True
pc = 0

#What arguments does SAVE need to
#save the number to register 2
# Registers use as variables
# R0-R7 These would be physically with cpu
registers = [None]*8

while running:
    '''I chose to make sure not to use variable names
    inside this logic, just to make sure I understood it
    
    memory[pc] is current command
    memory[pc+1] in PRINT_NUM and SAVE will be an interger used by command
    memory[pc+2] in SAVE will be a register to save variables to
    memory[pc+1] in PRINT_REGISTER is register index to be printed'''
    if memory[pc] == PRINT_GWEN:
        print("Gwen!")
        pc+=1

    if memory[pc] == PRINT_NUM:
        print(memory[pc+1])
        pc+=2

    if memory[pc] == SAVE:
        registers[memory[pc+2]] = memory[pc+1]
        print(f'Saved {memory[pc+1]}')
        pc+=3

    if memory[pc] == PRINT_REGISTER:
        print(registers[memory[pc+1]])
        pc+=2

    
    if memory[pc] == HALT:
        print('Halting!')
        running = False



