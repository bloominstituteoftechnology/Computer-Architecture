"""CPU functionality."""

import sys
HLT = 0b00000001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        """
        * `PC`: Program Counter, address of the currently executing instruction
        * `IR`: Instruction Register, contains a copy of the currently executing instruction
        * `MAR`: Memory Address Register, holds the memory address we're reading or writing
        * `MDR`: Memory Data Register, holds the value to write or the value just read
        * `FL`: Flags, see below
        """
        self.reg = [0]*8
        self.ram = [0]*256
        self.PC = 0
        self.IR = 0
        self.MAR = 0
        self.MDR = 0
        self.FL = 0
        self.instructions = {0b10000010: self.LDI, 0b01000111: self.PRN}

    def LDI(self, register, value):
        self.reg[register] = value

    def PRN(self, register):
        print(self.reg[register])

    def ram_read(self, address):
        """Accepts the adress to read and returns it's value"""
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        self.MAR = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[self.MAR] = instruction
            self.MAR += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            # self.fl,
            # self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.PC = 0
        while self.PC<len(self.ram):
            self.IR = self.PC
            value = self.ram[self.IR]
            # print(value)
            if value == HLT:
                return
            elif value in self.instructions:
                num_of_operands = (value & 0b11000000) >> 6
                # print(f"{value:b}, {num_of_operands:b}")
                if num_of_operands==2:
                    self.instructions[value](self.ram[self.IR+1],self.ram[self.IR+2])
                elif num_of_operands==1:
                    self.instructions[value](self.ram[self.IR+1])
                else:
                    self.instructions[value]()
            self.PC+=1

