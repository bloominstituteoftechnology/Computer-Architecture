
Computer arch topics we have implemented in our project
- RAM, self.ram
- registers!
- CPU, self.run
- ALU
Why LS8?
- 8 bits
- not the registers, as you might think
- Also, 8-bit CPU and ALU architectures are those that are based on registers,
address buses, or data buses of that size
    CPU
 00000000
 00000000
 00000000
 00000000
    RAM
- with 8-bit address bus, the CPU can address 256 bytes of RAM
General purpose calculating machine vs specialized calculating machines
           "computer"                               "calculator"
        Can do anything                         hardwired for specific calculations
        Broadly applicable                              Faster (often)
More memory? Stack!
- more variables
- function calls and nested function calls
To make a stack?
- Push
- Pop
- Memory space
-- RAM
-- 0-255 (256 bytes)
- a pointer to track where the top of the stack
-- variable that is a memory address
how to push
how to Pop
Handling 'leftovers' from push
Stack underflow
Why doesn't the CPU prevent underflow, or prevent wrapping around in memory?
- don't want the CPU to spend time/energy checking
- used to be dev's job, now it's the compiler's job
Stack overflow
- software's job to prevent this
Stacks and nested function calls
self.ram = [0] * 256
registers[7] = F3
SP = F3
memory[SP]
FF: 00
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
F4: 00
F3: 42    <--- SP
F2: 42
F1: 42
F0: 00
EF: 00
EE: 00
ED: 00
EC: 00
.
.
.
2B: 42
2A: 42 
.
.
.
10: 42
9: 42 
8: 42 
7: JUMP
6: R3
5: PUSH
4: R3 
3: 42
2: SAVE
1: PRINT_TIM
0: PRINT_TIM 
R0: 99
R1: 42
R3: 42
PUSH R0:
- decrement the SP
- copy the value from the given register
PUSH R1:
- decrement the SP
- copy the value from the given register
POP R3:
- copy into the register
- increment SP
PUSH R0:
- decrement the SP
- copy the value from the given register
POP R3:
- copy into the register
- increment SP
Stack
700: 4
699:  2   
698: 3
697: 6 
696: 6 
695: 7 <-- SP
694: 3 
693: 6
registers[4] = 6
a = 4
def mult(x, y):
   z = x * y
   return z
def main():
    a = 2
    b = 3
    c = a * b
    d = mult(a, b)
    e = 7
