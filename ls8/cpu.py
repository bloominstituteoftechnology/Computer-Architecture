"""CPU functionality."""

import sys
import re

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Initialize Register
        self.reg = [0] * 8

        # Initialize Memory
        self.ram = [0] * 256

        # Initialize internal registers
        self.pc = 0
        self.ir = 0
        self.mar = 0
        self.mdr = 0
        self.fl = 0

        # Initialize operation values
        self.operand_a = 0
        self.operand_b = 0

        # Initialize halt as false. CPU does not start halted

        self.halt = False

        # Initialize branch_table
        self.branch_table = {}
        self.branch_table[0b10000010] = self.LDI
        self.branch_table[0b01000111] = self.PRN
        self.branch_table[0b00000001] = self.HLT
        self.branch_table[0b10100010] = self.MUL


    def load(self, program):
        """Load a program into memory."""

        address = 0


        for instruction in program:
            self.ram_write(address, instruction)
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

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

    def ram_read(self, address):
        """
        Function that reads from memory. Takes in the address to read.
        Returns the value stored at that address in the RAM.
        """
        self.mdr = self.ram[address]

        return self.mdr

    def ram_write(self, address, value):
        """
        Function that writes to memory. Takes in the value to write,
        the address to write to. Saves value at the given address.
        """

        self.ram[address] = value
        self.mdr = self.ram[address]

    def run(self):
        """Run the CPU."""

        while not self.halt:         
            self.mar = self.pc
            self.ir = self.ram_read(self.mar)
            self.operand_a = self.ram_read(self.pc+1)
            self.operand_b = self.ram_read(self.pc+2)

            self.branch_table[self.ir]()

    def LDI(self):
        """
        Set register to this value
        """
        self.reg[self.operand_a] = self.operand_b
        self.pc += 3

    def PRN(self):
        """
        Prints numeric value stored at register address
        """
        print(self.reg[self.operand_a])
        self.pc += 2

    def HLT(self):
        """
        Sets halt value to true
        """
        self.halt = True
    
    def MUL(self):
        """
        Multiplies two numbers together.
        """
        self.reg[self.operand_a] *= self.reg[self.operand_b]
        self.pc += 3