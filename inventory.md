Inventory Step

CS Computer Architecture Repo asm --- ls8 --- examples folder (call, interrupts, keyboard, mult, print8, printstr, sctest, stack, stackoverflow) --- 
README: LS8 emulator project details --- cpu.py: CPU class (needs to be developed) --- ls8.py: where file will be run FAQ LS8-cheatsheet.md 
LS8-spec.md: Registers, Internal Registers, Flags, Stack, Interrupts, README.md - objectives for modules 1-4

ADD regA regB: add reg A and reg B, store in reg A
AND regA regB: bitwise-AND values in reg A and B, store in reg A
CALL register: call register
CMP regA regB: compare reg A and reg B, for equal, less than, greater than
DEC register: decrement the value in the register
DIV regA regB: reg A/reg B, store in reg A, if 0 print error and halt
HLT: halts CPU and exits emulator
INC register: increment the value in the given register
INT register: issue interrupt number stored in given register
IRET: return from interrupt handler
JEQ register: if equal flag is set to true, jump to address stored in given register
JGE register: if greater than flag or equal flag is set to true, jump to address stored in given register
JLE register: if less than or equal flag is set to true, jump to address stored in given register
JLT register: if less than flag is set to true, jump to address stored in given register
JMP register: jump to address stored in given register
JNE register: if equal flag is clear (false, 0) jump to address stored in given register
LD regA regB: loads regA with value at memory address stored in regB
LDI reg immediate: set value of a register to an interger
MOD regA regB (this instruction is handled by the ALU): divide value in the first register by the value in the second, storing the REMAINDER of the result in regA
MUL regA regB (this instruction is handled by the ALU): multiply the values in two registers together and store result in regA
NOP: no operation, do nothing for this instruction
NOT register (this instruction is handled by the ALU): perform bitwise not on value in register
OR regA regB (this is an instruction handled by the ALU): perform a bitwise-OR between values in regA and regB, storing result in regA
POP register: pop value at top of stack into given register
    1. copy value from address (pointed to by SP) to the given register
    2. increment SP
PRA register (pseudo-instruction): print alpha character value stored in the given register. print to the colsole the ASCII character corresponding to the value in the register
PRN register (pseudo-instruction): print numeric value store in the given register. print to the console the decimal integer value that is stored in the given register
PUSH register: push the value in the given register on the stack
    1. decrement the SP
    2. copy the value in the given register to the address pointed to by SP
RET: return from subroutine. pop value from top of stack and store in PC
SHL (this is an instruction handled by the ALU): shift the value in regA left by the number of bits specified in regB, filling the low bits with 0
SHR (this is an instruction handled by the ALU): shift the value in regA right by the number of bits specified in regB, filling the highest bits with 0
ST regA regB: store value in regB in the address stored in regA
SUB regA regB (this is an instruction handled by the ALU): subtract the value in the second reg from the first, storing result in regA
XOR regA regB: perform a bitwise-XOR between the values in regA and regB, storing result in regA