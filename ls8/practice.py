import sys


PRINT_SENT = 1
HALT       = 2
PRINT_NUM  = 3

memory =[ # memory is an array of 0 and 1
    PRINT_SENT,
    PRINT_NUM,
    1,
    PRINT_NUM,
    12,
    PRINT_SENT,
    PRINT_NUM,
    37,
    HALT
]

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
    elif command == PRINT_NUM:
        num = memory[pc +1]
        print(num)
        pc +=2
    else:
        print(f"unknown instraction: {command}")
        sys.exit(1)

   
