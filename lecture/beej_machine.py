# lecture\beej_machine.py

# Instructions Lexicon

    # 1 - PRINT_BEEJ
    # 2 - HALT
    # 3 - SAVE_REG - stores value in a register
    # 4 - PRINT_REG - prints the register's decimal value

memory = [
    1,
    3,
    4,
    37,
    4,
    4,
    2
]

registers = [0] * 8 

running = True

# Program Counter, the index in the memory array of the current-ly executing instruction
pc = 0

while running:
    # Instruction Register
    ir = memory[pc]

    # PRINT_BEEJ
    if ir == 1:
        print("Beej!")
        pc += 1

    # HALT
    elif ir == 2:
        running = False

    # SAVE_REG
    elif ir == 3:
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        registers[reg_num] = value

        # 為了更加深入地瞭解以上的過程:

        # print("reg_num")
        # print("-------")
        # print(reg_num)

        # print("")

        # print("value")
        # print("-----")
        # print(value)

        # print("")

        # print("registers")
        # print("---------")
        # print(registers)
        pc += 3

    # PRINT_REG
    elif ir == 4:
        reg_num = memory[pc + 1]
        print(registers[reg_num])

        pc += 2
