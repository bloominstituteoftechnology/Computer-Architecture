PRINT_TIM = 0b01
HALT = 0b10
PRINT_NUM = 0b11
SAVE = 0b100
PRINT_REG = 0b101
ADD = 0b110

memory = [
    PRINT_TIM,
    PRINT_TIM,
    PRINT_TIM,
    PRINT_NUM,
    42,
    SAVE,
    2,
    99,
    PRINT_REG,
    2,
    SAVE,
    3,
    1,
    ADD,
    2, 
    3,
    PRINT_REG,
    2,
    HALT
]

#representation of CPU memory 
registers = [0] * 8 

pc = 0
running = True
while running:
    command = memory[pc]

    if command == PRINT_TIM:
        print("Tim")
    
    if command == HALT:
        running = False

    if command == PRINT_NUM:
        pc += 1
        print(memory[pc])

    if command == SAVE:
        pc += 1
        registers[memory[pc]] = memory[pc+1]
        print(registers)
        pc += 1

    if command == PRINT_REG:
        to_print = memory[pc+1]
        print(registers[to_print])
        pc += 1

    if command == ADD:
        pc += 1
        registers[memory[pc]] = registers[memory[pc]] + registers[memory[pc+1]]
        pc += 1
    
    pc += 1

print("finished")


PRINT_TIM    =  0b00000001
HALT         =  0b10  # 2
PRINT_NUM    =  0b00000011  # opcode 3
SAVE         =  0b100
PRINT_REG    =  0b101    # opcode 5
ADD          =  0b110


# registers[2] = registers[2] + registers[3]

memory = [
    PRINT_TIM,
    PRINT_TIM,
    PRINT_NUM,
    42,
    SAVE,
    2,       # register to put it in
    99,      # number to save
    SAVE,
    3,      # register to save in
    1,      # number to save
    ADD,
    2,   # register to look at, and save stuff in
    3,   # register to look at
    PRINT_REG,
    2,       # register to look at
    HALT,
          ]

# write a program to pull each command out of memory and execute
# We can loop over it!

# register aka memory
registers = [0] * 8
# [0,0,99,0,0,0,0,0]
# R0-R7


# pc = 0  # program counter
# running = True
# while running:
#     command = memory[pc]

#     if command == PRINT_TIM:
#         print("Tim!")

#     if command == HALT:
#         running = False

#     if command == PRINT_NUM:
#         num_to_print = memory[pc + 1]
#         print(num_to_print)
#         pc += 1

#     if command == SAVE:
#         reg = memory[pc + 1]
#         num_to_save = memory[pc + 2]
#         registers[reg] = num_to_save

#         pc += 2

#     if command == PRINT_REG:
#         reg_index = memory[pc + 1]
#         print(registers[reg_index])
#         pc += 1

#     if command == ADD:
#         first_reg = memory[pc + 1]
#         sec_reg = memory[pc + 2]
#         registers[first_reg] = registers[first_reg] + registers[sec_reg]
#         pc += 2

#     pc += 1