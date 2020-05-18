# Number Bases 

Could we use this week to build an OS?
- It's the first step, but... eh, no?

### Base 2
- Binary!

### Base 8
- Octal (rare these days)

### Base 10
- Decimal! 

### Base 16
- Hexadecimal!

### Base 64
- Base 64

### What does it mean to count in bases?

Base 10
 0
 1
 2
 3
 4
 5
 6
 7
 8
 9
If I have ten of something
10
One tens and zero ones
It's not the tens place, it's how many tens we have

+---------- 1000's place
|+--------- 100's place
||+-------- 10's place
|||+------- 1's place
||||
abcd

1234

1 * 1000 + 2 * 100 + 3 * 10 + 4 * 1 == 1234

Base 2
  0
  1
 10
 11
100
You're adding another two's place every time you run out of digits

**You must be explicit if you are talking about writing a number in another base in Python**
- This is done by writing '0b' in front of the binary number
0b101 = 5
1 in the 4s place
0 in the 2s place
1 in the 1s place

+---------- 8's place 2^3
|+--------- 4's place 2^2
||+-------- 2's place 2^1
|||+------- 1's place 2^0
||||
1010

This is 2^n where n is the place
This is ten!

1100 --> 12 

1 * 8 + 1 * 4 + 0 + 0 == 12

## A simple CPU
### A program that pretends to be a CPU

I want to:
- Store a sequence of instructions
- Go through those instructions, doing whatever they ask me to do

Instructions:
- Print "Mack" on the screen three times
- Halts the program

_Psuedocode in Python_
```
PRINT_MACK = 1
HALT = 2

memory = [
    # PRINT_MACK 1
    # PRINT_MACK 1
    # PRINT_MACK 1
    # HALT 
]
Let's say 1 represents Print Mack
2 shall represent Halt

halted = False

pc = 0 # "Program Counter": Index into the memory array AKA a pointer, address, location

while not halted:
    instruction = memory[pc]

    if instruction == PRINT_MACK:
        print("Mack!")
    elif instruction == HALT:
        halted = True
    else:
        print(f'Unknown instruction: {instruction} at address {pc})
        sys.exit(1)
```