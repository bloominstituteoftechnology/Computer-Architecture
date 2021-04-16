"""CPU functionality."""
#
import sys

#instruction set:
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101 
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.sp = 0 #set it to the first one in the stack?
        self.fl = 0

        self.reg[self.sp] = 0xf4

#originally this part is `hardcoded` and needs the parser instead

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0 #constant ram address
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num == '':
                        continue

                    self.ram[address] = int(num, 2)
                    address += 1

        except FileNotFoundError:
            print("file not found")
            sys.exit(2)

      
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, newvalue, address):
        self.ram[address] = newvalue

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
            print()

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        running = True
        while running:
            instruction = self.ram[self.pc]
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]
# LDI
            if instruction == LDI:
                reg_index = operand_a
                num = operand_b
                self.reg[reg_index] = num
                self.pc += 3
# PRN
            elif instruction == PRN:
                reg_index = operand_a
                num = self.reg[reg_index]
                print(num)
                self.pc += 2
#MUL
            elif instruction == MUL:
                self.alu("MUL", operand_a, operand_b)
#PUSH       
            elif instruction == PUSH:
                reg_index = operand_a
                val = self.reg[reg_index]
                
                self.reg[self.sp] -= 1

                self.ram[self.reg[self.sp]] = val
                self.pc += 2
#POP
            elif instruction == POP:
                reg_index = operand_a

                self.reg[reg_index] = self.ram[self.reg[self.sp]]

                self.reg[self.sp] += 1
                self.pc += 2
# HLT
            elif instruction == HLT:
                running = False
                sys.exit(0)
# CALL
            elif instruction == CALL:
                address_to_return_to = self.pc + 2
                self.reg[self.pc] -= 1
                self.ram[self.reg[self.sp]] = address_to_return_to
                reg_index = operand_a
                address_to_call = self.reg[reg_index]
                self.pc = address_to_call
# RET
            elif instruction == RET:
                self.pc = self.ram[self.reg[self.sp]]
                self.reg[self.sp] + 1
#

            else:
                print("WRONG WAY")
                sys.exit(1)