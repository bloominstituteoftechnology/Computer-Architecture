"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        
        # RAM
        self.ram = [0] * 256

        # general-purpose registers
        self.registers = [0] * 8
        self.registers[7] = 0xF4    # stack pointer

        # internal registers
        self.pc = None   # program counter
        self.ir = None   # instruction register
        self.mar = None  # memory address register
        self.mdr = None  # memory data register
        self.fl = None   # flags

    # retrieve the value stored in the MAR register, and store it in the MDR register
    def ram_read(self):
        self.mdr = self.ram[self.mar]

    # write the value stored in the MDR register into the MAR register
    def ram_write(self):
        self.ram[self.mar] = self.mdr

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

    def run(self):
        """Run the CPU."""
        pass
