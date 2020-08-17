memory = [
    1, # print
    1, # print
    1, # print
    1, # print
    3, # save reg R2, 99
    2, # halt
    99, # value
    4, # print reg2
    2,
    2 # halt
]

register = [0] * 8

pc = 0

running = True

while running:
    inst = memory[pc]

    if inst == 1:
        print("1 Beej")
        pc += 1

    elif inst == 2:
        running = False

    elif inst == 3: # save reg
        reg_num = memory[pc + 1]
        value = memory[pc + 2]

        register[reg_num] = value

        pc += 3

    elif inst == 4:
        reg_num = memory[pc + 1]
        print(register[reg_num])
        pc += 2

