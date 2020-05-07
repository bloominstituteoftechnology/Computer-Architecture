import sys


PRINT_SENT     = 1
HALT           = 2
PRINT_NUM      = 3
SAVE           = 4 # save a value to a register
PRINT_REGISTER = 5 # print a  value from a register
ADD            = 6 # regA += regB  add some values from regA to regB

#! very slow comparing to a register
memory =[ # memory is an array of 0 and 1 or RAM
    PRINT_SENT,
    SAVE,
    65, #value
    2, #register
    SAVE,
    20, #Value
    3, # register
    ADD,
    2, #register
    3, #register
    PRINT_REGISTER,
    2, #register
    HALT
]

#! 8 bit register
register = [0] * 8 # register memory are halt or built in the hard ware, fast and small
# register represent numbers from 0 to 7


#  need to have a pointer to tell us which instruction 
pc = 0 # PC program counter starts from 0. 

running = True

while running:# this is a processor 
    command = memory[pc]

    if command == PRINT_SENT:
        print("SENT !!") 
        pc+=1

    elif command == HALT:
        running = False
    # elif command == PRINT_NUM:
    #     num = memory[pc +1]
    #     print(num)
    #     pc +=2

#! SAVE
    elif command == SAVE:
        num = memory[pc + 1]
        reg = memory[pc + 2]
        register[reg] = num
        pc +=3


    elif command == PRINT_REGISTER:
        reg = memory[pc + 1]
        print(register[reg])
        pc += 2

#! ADD
    elif command == ADD:
        reg_a = memory[pc + 1]
        reg_b = memory[pc + 2]
        register[reg_a] += register[reg_b]
        pc += 3
    else:
        print(f"unknown instraction: {command}")
        sys.exit(1)

   
