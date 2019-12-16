"""CPU functionality."""

import sys

# No-op
NOP = 0b00000000  # Takes no parameters

# Halt
HLT = 0b00000001  # Takes no parameters

# LDI Register Immediate
# Set the value of a register to an integer.
# Parameter 1: Register #
# Parameter 2: Value to store in register
LDI = 0b10000010  # Takes 2 parameters

LD = 0b10000011  # Takes 2 parameters
ST = 0b10000100  # Takes 2 parameters

PUSH = 0b01000101  # Takes 1 parameter
POP = 0b01000110  # Takes 1 parameter

# Print
# Print numeric value stored in the given register.
PRN = 0b01000111  # Takes 1 parameter
PRA = 0b01001000  # Takes 1 parameter


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = {}
        self.reg = [0] * 8
        self.__pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8 - 130
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0 - 71
            0b00000000,
            0b00000001,  # HLT - 1
        ]

        for instruction in program:
            print("address: ", address)
            self.ram[address] = instruction
            address += 1

    def ram_read(self):
        pass

    def ram_write(self):
        pass

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
        running = True

        while running:
            instruction = self.ram[self.__pc]

            if instruction is HLT:
                running = False

            elif instruction is LDI:
                register_num = self.reg[self.__pc + 1]
                self.reg[register_num] = self.ram[self.__pc + 2]
                self.__pc += 3

            elif instruction is PRN:
                key = self.ram[self.__pc + 1]
                register_num = self.reg[self.__pc + 1]
                self.__pc += 2

            else:
                print(f"Unknown instruction at index {self.__pc}")
                sys.exit(1)
