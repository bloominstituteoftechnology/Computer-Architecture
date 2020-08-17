"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.mar = 0
        self.mdr = 0

    def load(self):
        """Load a program into memory."""

        address = 0

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
            self.ram[address] = instruction
            address += 1

    def ram_read(self, addr):
        return self.ram[addr]

    def ram_write(self, addr, val):
        self.ram[addr] = val

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
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        # Microcode
        def HLT():
            return False

        def LDI():
            self.mar = self.ram[self.pc + 1]
            self.mdr = self.ram[self.pc + 2]
            self.reg[self.mar] = self.mdr
            return 3

        def PRN():
            self.mar = self.ram[self.pc + 1]
            self.mdr = self.reg[self.mar]
            print(self.mdr)
            return 2

        # Instruction mapping
        instructions = {
            0x01: HLT,
            0x82: LDI,
            0x47: PRN,
        }
        
        # Execution loop
        while True:
            ir = self.ram[self.pc]
            step = instructions[ir]()
            if not step:
                break
            self.pc += step
