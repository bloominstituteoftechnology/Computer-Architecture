"""CPU functionality."""
#
import sys

#instruction set:
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.registers = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

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

                    ram[address] = int(num)
                    address += 1

        except FileNotFoundError:
            print("file not found")
            sys.exit(2)

    load(filename)
      
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

#From the spec:
#When the LS-8 is booted, the following steps occur:

#R0-R6 are cleared to 0.
#R7 is set to 0xF4.
#PC and FL registers are cleared to 0.
#RAM is cleared to 0.
#Subsequently, the program can be loaded into RAM starting at address 0x00.

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
                self.registers[reg_index] = num
                self.pc += 3
# PRN
            elif instruction == PRN:
                reg_index = operand_a
                num = self.registers[reg_index]
                print(num)
                self.pc += 2
#MUL
            elif instruction == MUL:
                reg_index = operand_a
                reg_index = operand_b
                alu("MUL", self.reg_a, self.reg_b)
# HLT
            elif instruction == HLT:
                running = False
                sys.exit(0)

            else:
                print("WRONG WAY")
                sys.exit(1)