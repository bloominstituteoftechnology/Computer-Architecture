# The index in the memory array, aka location, address, pointer

#1 print beej
#2 halt
# 3 Store_reg store a value in a register

memory = [  # big array of bytes 8 bits per byte
    1, # print beej
    3, # store in reg r4 37
    4, # 4 and 37 are args for savereg also called operands
    37,
    2 # halt
]
"""
    registers[3] = 37
"""

registers = [0] * 8  #  cpu registers/ like variables hard coded

running = True

pc = 0  # index in memory that is currently executing / program counter

while running:
    ir = memory[pc]  # instruction register (inside cpu)

    if ir == 1:
        print('Beej')
        pc += 1
    elif ir == 2:
        running = False
        pc += 1
    elif ir == 3:
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        registers[reg_num] = value
        print(f"{registers[reg_num]}")
        pc += 3
        