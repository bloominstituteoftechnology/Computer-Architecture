"""
----------------------
OPCODES (Instructions)
----------------------
1. Basic
"""
# No operation. Do nothing for this instruction.
# Machine code:
# 00000000
# 00
NOP         = 0b00000000

# HLT
# Halt the CPU (and exit the emulator).
# Machine code:
# 00000001 
# 01
HLT         = 0b00000001

# INT register
# Issue the interrupt number stored in the given register.
# This will set the _n_th bit in the IS register to the value in the given register.
# Machine code:
# 01010010 00000rrr
# 52 0r
INT         = 0b01010010

# IRET
# Return from an interrupt handler.
# The following steps are executed:
# Registers R6-R0 are popped off the stack in that order.
# The FL register is popped off the stack.
# The return address is popped off the stack and stored in PC.
# Interrupts are re-enabled
# Machine code:
# 00010011
# 13
IRET        = 0b00010011

# CALL register
# Calls a subroutine (function) at the address stored in the register.
# The address of the instruction directly after CALL is pushed onto the stack. This allows us to return to where we left off when the subroutine finishes executing.
# The PC is set to the address stored in the given register. We jump to that location in RAM and execute the first instruction in the subroutine. The PC can move forward or backwards from its current location.
# Machine code:
# 01010000 00000rrr
# 50 0r
CALL        = 0b01010000

"""
2. Memory Read/Write
"""
# LD registerA registerB
# Loads registerA with the value at the memory address stored in registerB.
# This opcode reads from memory.
# Machine code:
# 10000011 00000aaa 00000bbb
# 83 0a 0b
LD          = 0b10000011

# LDI register immediate
# Set the value of a register to an integer.
# Machine code:
# 10000010 00000rrr iiiiiiii
# 82 0r ii
LDI         = 0b10000010

# ST registerA registerB
# Store value in registerB in the address stored in registerA.
# This opcode writes to memory.
# Machine code:
# 10000100 00000aaa 00000bbb
# 84 0a 0b
ST          = 0b10000100

"""
3. Stack Manipulation
"""
# PUSH register
# Push the value in the given register on the stack.
# Decrement the SP.
# Copy the value in the given register to the address pointed to by SP.
# Machine code:
# 01000101 00000rrr
# 45 0r
PUSH        = 0b01000101

# RET
# Return from subroutine.
# Pop the value from the top of the stack and store it in the PC.
# Machine Code:
# 00010001
# 11
RET         = 0b00010001

# POP register
# Pop the value at the top of the stack into the given register.
# Copy the value from the address pointed to by SP to the given register.
# Increment SP.
# Machine code:
# 01000110 00000rrr
# 46 0r
POP         = 0b01000110

"""
4. Jump & Conditional Jump
"""
# JMP register
# Jump to the address stored in the given register.
# Set the PC to the address stored in the given register.
# Machine code:
# 01010100 00000rrr
# 54 0r
JMP         = 0b01010100

# JEQ register
# If equal flag is set (true), jump to the address stored in the given register.
# Machine code:
# 01010101 00000rrr
# 55 0r
JEQ         = 0b01010101

# JNE register
# If E flag is clear (false, 0), jump to the address stored in the given register.
# Machine code:
# 01010110 00000rrr
# 56 0r
JNE         = 0b01010110

# JGE register
# If greater-than flag or equal flag is set (true), jump to the address stored in the given register.
# 01011010 00000rrr
# 5A 0r
JGE         = 0b01011010

# JGT register
# If greater-than flag is set (true), jump to the address stored in the given register.
# Machine code:
# 01010111 00000rrr
# 57 0r
JGT         = 0b01010111

# JLE register
# If less-than flag or equal flag is set (true), jump to the address stored in the given register.
# 01011001 00000rrr
# 59 0r
JLE         = 0b01011001

# JLT register
# If less-than flag is set (true), jump to the address stored in the given register.
# Machine code:
# 01011000 00000rrr
# 58 0r
JLT         = 0b01011000

"""
I/O Instructions
"""
# PRA register pseudo-instruction
# Print alpha character value stored in the given register.
# Print to the console the ASCII character corresponding to the value in the register.
# Machine code:
# 01001000 00000rrr
# 48 0r
PRA         = 0b01001000

# PRN register pseudo-instruction
# Print numeric value stored in the given register.
# Print to the console the decimal integer value that is stored in the given register.
# Machine code:
# 01000111 00000rrr
# 47 0r
PRN         = 0b01000111

"""
ALU Instructions
"""
# This is an instruction handled by the ALU.
# ADD registerA registerB
# Add the value in two registers and store the result in registerA.
# Machine code:
# 10100000 00000aaa 00000bbb
# A0 0a 0b
ADD         = 0b10100000

# This is an instruction handled by the ALU.
# AND registerA registerB
# Bitwise-AND the values in registerA and registerB, then store the result in registerA.
# Machine code:
# 10101000 00000aaa 00000bbb
# A8 0a 0b
AND         = 0b10101000

# This is an instruction handled by the ALU.
# CMP registerA registerB
# Compare the values in two registers.
# If they are equal, set the Equal E flag to 1, otherwise set it to 0.
# If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
# If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
# Machine code:
# 10100111 00000aaa 00000bbb
# A7 0a 0b
CMP         = 0b10100111

# This is an instruction handled by the ALU.
# DEC register
# Decrement (subtract 1 from) the value in the given register.
# Machine code:
# 01100110 00000rrr
# 66 0r
DEC         = 0b01100110

# This is an instruction handled by the ALU.
# DIV registerA registerB
# Divide the value in the first register by the value in the second, storing the result in registerA.
# If the value in the second register is 0, the system should print an error message and halt.
# Machine code:
# 10100011 00000aaa 00000bbb
# A3 0a 0b
DIV         = 0b10100011

# This is an instruction handled by the ALU.
# INC register
# Increment (add 1 to) the value in the given register.
# Machine code:
# 01100101 00000rrr
# 65 0r
INC         = 0b01100101

# This is an instruction handled by the ALU.
# MOD registerA registerB
# Divide the value in the first register by the value in the second, storing the remainder of the result in registerA.
# If the value in the second register is 0, the system should print an error message and halt.
# Machine code:
# 10100100 00000aaa 00000bbb
# A4 0a 0b
MOD         = 0b10100100

# This is an instruction handled by the ALU.
# MUL registerA registerB
# Multiply the values in two registers together and store the result in registerA.
# Machine code:
# 10100010 00000aaa 00000bbb
# A2 0a 0b
MUL         = 0b10100010

# This is an instruction handled by the ALU.
# NOT register
# Perform a bitwise-NOT on the value in a register, storing the result in the register.
# Machine code:
# 01101001 00000rrr
# 69 0r
NOT         = 0b01101001

# This is an instruction handled by the ALU.
# OR registerA registerB
# Perform a bitwise-OR between the values in registerA and registerB, storing the result in registerA.
# Machine code:
# 10101010 00000aaa 00000bbb
# AA 0a 0b
OR          = 0b10101010

# This is an instruction handled by the ALU.
# Shift the value in registerA left by the number of bits specified in registerB, filling the low bits with 0.
# 10101100 00000aaa 00000bbb
# AC 0a 0b
SHL         = 0b10101100

# This is an instruction handled by the ALU.
# Shift the value in registerA right by the number of bits specified in registerB, filling the high bits with 0.
# 10101101 00000aaa 00000bbb
# AD 0a 0b
SHR         = 0b10101101

# This is an instruction handled by the ALU.
# SUB registerA registerB
# Subtract the value in the second register from the first, storing the result in registerA.
# Machine code:
# 10100001 00000aaa 00000bbb
# A1 0a 0b
SUB         = 0b10100001

# This is an instruction handled by the ALU.
# XOR registerA registerB
# Perform a bitwise-XOR between the values in registerA and registerB, storing the result in registerA.
# Machine code:
# 10101011 00000aaa 00000bbb
# AB 0a 0b
XOR         = 0b10101011

"""
END OPCODE TABLE 
""" 