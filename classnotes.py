import sys
# memory is a big array of bytes (8 bits each).  It has an "index" and a value.  

# the index is also known as the location, pointer or address

# capacitors hold a charge for 1 or no-charge for 0 at the hardware level.

# 1 - PRINT_BEEJ  <-- our instructions
# 2 - HALT
# 3 - SAVE_REG store a value in a register
# 4 - PRINT_REG
# 5 - PUSH
# 6 - POP


# We're writing a program that goes through memory, interprets the value, and executes the instruction.

memory = [0] * 256

registers = [0] * 8  # the 8 slots we have "on the CPU" in our example program (LS8)

registers[7] = 0xf4  # stack pointer

address = 0

if len(sys.argv) != 2:  
    print("usage invalid")
    sys.exit(1)

try: 
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.strip()
            temp = line.split()

            if len(temp) == 0:
                continue

            if temp[0][0] == '#':
                continue

            try:
                memory[address] = int(temp[0])

            except ValueError:
                print(f"invalid number: {temp[0]}")
                sys.exit(1)

            address += 1

except FileNotFoundError:
    print(f"Couldn't open {sys.argv[1]}")
    sys.exit(2)

running = True

pc = 0 # Program Counter is the index into memory of the currently executing instruction

while running:
    ir = memory[pc] # Instruction Register - internal part of CPU that holds a value.  Special purpose part of CPU.

    if ir == 1: # PRINT_BEEJ
        print("Beej")
        pc += 1

    elif ir == 2: # HALT
        running = False
        pc += 1

    elif ir == 3: # SAVE_REG
        reg_num = memory[pc+1]
        value = memory[pc+2]
        registers[reg_num] = value
        # print(f"{registers[reg_num]}")
        pc += 3

    elif ir == 4: #PRINT_REG
        reg_num = memory[pc+1]
        print(registers[reg_num])
        pc += 2

    elif ir == 5: # PUSH
        registers[7] -= 1 # decriment SP (stack pointer)
        reg_num = memory[pc + 1]   # get value from register
        value = registers[reg_num] # we want to push this value
        top_of_stack_addr = registers[7]         
        memory[top_of_stack_addr] = value # store at top of the stack
        pc += 2

    elif ir == 6: # POP
        top_of_stack_addr = registers[7]

        reg_num = memory[pc+1]

        registers[reg_num] = memory[top_of_stack_addr]

        registers[7] += 1

        pc += 2

    elif ir == 7: # CALL
        # push return address
        ret_addr = pc + 2
        registers[7] -= 1
        memory[registers[7]] = ret_addr

        # call the subroutine
        reg_num = memory[pc+1]
        pc = registers[reg_num]

    elif ir == 8: # RET
        pass

    else:
        print(f"invalid instruction {ir} at address {pc}")
        sys.exit(1)

 




    

"""
"Registers" are memory actually on the CPU.  They are very fast.  We have a limited number in a CPU.  That is fixed based on how it is physically build.
In our example, LS8, they are called r0 to r7.


Bitwise Operations

first, Boolean

A  B      A and B
__________________
F  F         F
F  T         F
T  F         F
T  T         T


A  B      A or  B
__________________
F  F         F
F  T         T
T  F         T
T  T         T

A     NOT A
____________
T        F
F        T

then, Bitwise

A  B      A & B
__________________
0  0         0
0  1         1
1  0         1
1  1         2


A  B      A | B
__________________
0  0         0
0  1         1
1  0         1
1  1         2

A   ~A
________
1    0
0    1

BITWISE OR

 00011011000
| 11111110000
_____________
 11111111000

BIT SHIFTING
_____________

10101011
01010101
00101010
00010101

ANALOGY N BASE 10 OF EXTRACTING NUMBERS

1234567
^^

WANT TO EXTRACT THE 3 AND 4 ABOVE

0123456
0012345
0001234

1234567 // 1000

= 1234

IF YOU DIVIDE OR MULTIPLY BY THE BASE (1000 IN THIS CASE) YOU SHIFT LEFT AND RIGHT

1234567 // 0
1234

NOW IN BINARY

0101001010110
   ^^^^

Need to shift right by 6 to get our number

0101001

NOW NEED TO MASK THE FIRST 3 BITS OUT

  0101001
& 0001111
_________
  0001001
IS EQUIVALENT TO 1001
"""

"""
CPU STACK

> PUSH
> POP

Store pushed items in RAM
Pointer to the top of the stack
Pointer or address or index to a place in memory are equivalent

In LS8 computer we use register 7 (r7) to track top of the stack.

R7 and the Stack Pointer(SP) are the same thing.

R7: F4


Push: decriment the stack pointer (SP) and copy the value from the register to the address of the SP (ex. PUSH R0)
Pop: copy the value at the SP and copy into the register.  Increment the SP. (ex. POP R1)


Memory Map
----------

index: value
FF: 00  <-- FF in hexadecimal is = 255
FE: 00
FD: 00
FC: 00
FB: 00
FA: 00
F9: 00
F8: 00
F7: 00
F6: 00
F5: 00
F4: 00 <-- SP (stack pointer)
F3: 00
F2: 00
F1: 00
F0: 00
EF: 00
.
.
.
05: 00
04: XX
03: XX
02: XX
01: XX
00: XX <-- PC (current instruction pointer)

XX are abitrary program instructions.



"""











