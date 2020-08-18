# 1 - PRINT_AARON
# 2 - HALT
# 3 - SAVE_REG --> store a value in a register
# 4 - PRINT_REG --> print the register value in decimal

memory = [
    1, #> PRINT_AARON

    3, #> SAVE_REG R4, 37; instruction itself, aka "opcode"
    4, #> 4 and 37 are arguments to SAVE_REG, aka "operands"
    37,

    4, #> PRINT_REG R4
    4, #> operand for opcode 4

    2  #> HALT
]

registers = [0] * 8

running = True

pc = 0 #> Program Counter: the index into memory of the currently
       #> executing instruction

while running:
    ir = memory[pc] #> the instruction register

    if ir == 1:
        print("AARON")
        pc += 1

    elif ir == 2:
        running = False
        pc += 1

    elif ir == 3: #> SAVE_REG
        reg_num = memory[pc + 1]
        reg_val = memory[pc + 2]
        registers[reg_num] = reg_val

        pc += 3 #> 3 byte instruction

    elif ir == 4: #> PRINT_REG
        reg_num = memory[pc + 1]
        print(registers[reg_num])

        pc += 2 #> 2 byte instruction