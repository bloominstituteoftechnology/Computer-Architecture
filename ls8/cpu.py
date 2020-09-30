"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # creationg of the register
        self.reg = [0] * 8 # the register is 8 bits long
        self.ram = [0] * 256 # this the memory or the ram
        self.pc = 0 # this the program counter

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
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


    def ram_read(self, mem_add_reg):
        return self.ram[mem_add_reg]


    def ram_write(self, mem_dat_reg, mem_add_reg):
        self.ram[mem_add_reg] = mem_dat_reg


    def run(self):
        """Run the CPU."""

        # here is where we will store the 
        # name with the number of each action
        # to perform
        
        ir = self.ram_read(self.pc)

        running = True
        
        # Loop for the program to run
        while running:

