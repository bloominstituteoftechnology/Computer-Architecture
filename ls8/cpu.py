"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256-byte RAM, each element is 1 byte (can only store integers 0-255)
        self.ram = [0] * 256

        # R0-R7: 8-bit general purpose registers, R5 = interrupt mask (IM), 
        # R6 = interrupt status (IS), R7 = stack pointer (SP)
        self.reg = [0] * 8

        # Internal Registers
        self.pc = 0 # Program Counter: address of the currently executing instruction
        self.ir = 0 # Instruction Register: contains a copy of the currently executing instruction
        self.mar = 0 # Memory Address Register: holds the memory address we're reading or writing
        self.mdr = 0 # Memory Data Register: holds the value to write or the value just read
        self.fl = 0 # Flag Register: holds the current flags status

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
    
    def ram_read(self, mar):
        if mar >= 0 and mar < len(self.ram):
            return self.ram[mar]
        else:
            print(f"Error: Attempted to read from memory address: {mar}, which is outside of the memory bounds.")
            return -1

    def ram_write(self, mar, mdr):
        if mar >= 0 and mar < len(self.ram):
            self.ram[mar] = mdr & 0xFF
        else:
            print(f"Error: Attempted to write to memory address: {mar}, which is outside of the memory bounds.")