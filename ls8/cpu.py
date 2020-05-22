"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
MUL = 0b10100010
POP = 0b01000110
PRN = 0b01000111
PUSH = 0b01000101

SP = 7 # register number for stack pointer

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        self.branch = {LDI: self.ldi,
                       MUL: self.mul,
                       POP: self.pop,
                       PRN: self.prn,
                       PUSH: self.push,
                       }

        self.reg = bytearray(8)
        self.ram = bytearray(256)
        
        self.reg[SP] = 0xF4

        self.PC = 0
        self.IR = 0
        self.MAR = 0
        self.MDR = 0
        self.FL = 0

    def ldi(self, reg_num, value):
        self.reg[reg_num] = value

    def mul(self, reg_a_num, reg_b_num):
        self.alu("MUL", reg_a_num, reg_b_num)

    def pop(self, reg_num):
        self.reg[reg_num] = self.ram_read(self.reg[SP])
        self.reg[SP] += 1

    def prn(self, reg_num):
        print(self.reg[reg_num])
        
    def push(self, reg_num):
        self.reg[SP] -= 1
        self.ram_write(self.reg[reg_num], self.reg[SP])

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("Usage: ls8.py <filename>")
            sys.exit()

        with open(sys.argv[1]) as file:
            program = [int(line[:line.find('#')].strip(), 2)
                       for line in file
                       if line != '\n' and line[0] != '#']

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()

    def run(self):
        """Run the CPU."""
        self.IR = self.ram_read(self.PC)
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)

        while self.IR != HLT:
            num_args = (self.IR & 0b11000000) >> 6
            try:
                if num_args == 0:
                    self.branch[self.IR]()
                elif num_args == 1:
                    self.branch[self.IR](operand_a)
                else:
                    self.branch[self.IR](operand_a, operand_b)
            except KeyError:
                raise Exception("Unsupported operation.")

            self.PC += num_args + 1
            self.IR = self.ram_read(self.PC)
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)
