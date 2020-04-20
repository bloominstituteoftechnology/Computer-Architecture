# Write a program in python that runs programs

PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3  # Store a value in a register (in the LS8 called LDI)
PRINT_REG = 4  # corresponds to PRN in the LS8

# Where should we store instructions? What data structure makes sense?
# We want to store them in memory (similar to an indexed array), so we will use a list

memory = [
    PRINT_BEEJ,
    SAVE_REG,  # SAVE R0, 37    (store the value 37 in R0)     the opcode (the instruction byte itself)
    0,  # R0      operand("argument")
    37,  # 37      operand
    PRINT_BEEJ,
    PRINT_REG,  # PRINT_REG R0
    0,  # R0
    HALT,
]
register = [0] * 8  # registers are like variables. R0 - R7. They hold values.

# We can do this with a for loop, but it is inflexible. We can introduce a program counter≈
# for v in memory:
#     if v == PRINT_BEEJ:
#         print("Beej!")
#     elif v == HALT:
#         break

pc = 0  # program counter: address (memory index) of the current instruction
running = True

while running:
    inst = memory[pc]

    if inst == PRINT_BEEJ:
        print("Beej!")
        pc += 1  # moves us through all the instructions in memory array by index

    elif inst == SAVE_REG:  # pc is at SAVE_REG
        reg_num = memory[
            pc + 1
        ]  # so the reg number we want is one slot after pc in memory
        value = memory[pc + 2]  # and the value is two slots after pc in the register
        register[reg_num] = value
        pc += 3  # we incrememnt three to get to the next instruction after SAVE_REG, which is PRINT_BEEJ

    elif inst == PRINT_REG:
        reg_num = memory[pc + 1]
        value = register[reg_num]
        print(value)
        pc += 2

    elif inst == HALT:
        running = False

    else:
        print("unknown instruction")
        running = False
