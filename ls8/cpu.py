"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0        # Program Counter, address of the currently executing instruction
        self.IR = None     # Instruction Register, contains a copy of the currently executing instruction
        # MAR = None  # Memory Address Register, holds the memory address we're reading or writing
        # MDR = None  # Memory Data Register, holds the value to write or the value just read

        # R5 is reserved as the interrupt mask (IM)
        # R6 is reserved as the interrupt status (IS)
        # R7 is reserved as the stack pointer (SP)

    def ram_read(self, MAR):
        if MAR < len(self.ram):
            return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        if MAR < len(self.ram):
            self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""
        HTL = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111

        while True:
            inst = bin(self.ram[self.pc])
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR is HTL:
                self.hlt_inst()
            elif IR is PRN:
                self.prn_inst(operand_a)
            elif IR is LDI:
                self.ldi_inst(operand_a, operand_b)
            self.pc += 1

    def hlt_inst(self):
        exit(1)

    def ldi_inst(self, MAR, MDR):
        if MAR < len(self.ram):
            self.reg[MAR] = MDR

    def prn_inst(self, reg):
        print(self.reg[reg])

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
