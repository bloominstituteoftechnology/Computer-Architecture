"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        reg = [0] * 256
        ram = [0] * 256
        PC = 0        # Program Counter, address of the currently executing instruction
        IR = None     # Instruction Register, contains a copy of the currently executing instruction
        # MAR = None  # Memory Address Register, holds the memory address we're reading or writing
        # MDR = None  # Memory Data Register, holds the value to write or the value just read

        R0 = None
        R1 = None
        R2 = None
        R3 = None
        R4 = None
        R5 = None  # R5 is reserved as the interrupt mask (IM)
        R6 = None  # R6 is reserved as the interrupt status (IS)
        R7 = None  # R7 is reserved as the stack pointer (SP)

    def ram_read(self, MAR):
        return self.reg[MAR]

    def ram_write(self, MAR, MDR):
        self.reg[MAR] = MDR

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
        self.IR = self.PC
