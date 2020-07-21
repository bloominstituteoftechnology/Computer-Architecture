"""
CPU
    Executing instructions
    Gets them out of RAM
    Registers (like variables)
        Fixed names  R0-R7
        Fixed number of them -- 8 of them
        Fixed size -- 8 bits

Memory (RAM)
    A big array of bytes
    Each memory slot has an index, and a value stored at that index
    That index into memory AKA:
        pointer
        location
        address
"""

memory = [
    1,  # PRINT_BEEJ
    1,  # PRINT_BEEJ
    1,  # PRINT_BEEJ
    3,  # SAVE_REG R2,64  register to save in, the value save there
    2,  #          R2
    64, #             64
    4,  # PRINT_REG R2
    2,  #           R2
    2,  # HALT <-- pc
]

# for inst in memory:
#     if inst == 1:  # PRINT_BEEJ
#         print("Beej")

#     elif inst == 2:  # HALT
#         break

#     else:
#         print(f"Unknown instruction {inst}")

register = [0] * 8

pc = 0  # Program Counter, index into memory of the current instruction
        # AKA a pointer to the current instruction

running = True

while running:
    inst = memory[pc]

    if inst == 1:  # PRINT_BEEJ
        print("Beej")
        pc += 1

    elif inst == 2:  # HALT
        running = False

    elif inst == 3:  # SAVE_REG
        reg_num = memory[pc + 1]
        value = memory[pc + 2]

        register[reg_num] = value

        pc += 3

    elif inst == 4: # PRINT_REG
        reg_num = memory[pc + 1]
        print(register[reg_num])

        pc += 2

    else:
        print(f"Unknown instruction {inst}")

