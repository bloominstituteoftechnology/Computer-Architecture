
PRINT_MIKE = 0b01
HALT = 0b10 # 2
PRINT_NUM = 0b11 # 3
SAVE = 0b100 # 4
PRINT_REG = 0b101 # 5
ADD = 0b110 # 6


memory = [
    PRINT_MIKE,
    PRINT_MIKE,
    PRINT_NUM,
    42,
    SAVE,
    2,  # index of register to save into
    99, # value to save into register
    SAVE,
    3,  # index of register to save into
    1,  # number to save into register
    ADD,
    2, # index of register to get value
    3, # index of register to get value
    PRINT_REG,
    2,
    HALT,
]

registers = [0] * 8

# Write a program to pull each command out of memory and execute

pc = 0
running = True
while running:
    command = memory[pc]

    if command is PRINT_MIKE:
        print("Mike!")

    if command is HALT:
        running = False

    if command is PRINT_NUM:
        num_to_print = memory[pc + 1]
        print(num_to_print)
        pc += 1

    if command is SAVE:
        reg = memory[pc + 1]
        num_to_save = memory[pc + 2]
        registers[reg] = num_to_save
        pc += 2

    if command is PRINT_REG:
        reg_to_print = memory[pc + 1]
        print(registers[reg_to_print])
        pc += 1
    
    if command is ADD:
        first_reg = memory[pc + 1]
        second_reg = memory[pc + 2]
        
        registers[first_reg] = registers[first_reg] + registers[second_reg]
        pc += 2

    pc += 1


# Given the following array of values, print out all the elements in reverse order, with each element on a new line.
# For example, given the list
x = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
# x.reverse()
for num in x[::-2]:
    print(num)
# Your output should be
# 0
# 1
# 2
# 3
# 4
# 5
# 6
# 7
# 8
# 9
# 10
# You may use whatever programming language you'd like.
# Verbalize your thought process as much as possible before writing any code. Run through the UPER problem solving framework while going through your thought process.