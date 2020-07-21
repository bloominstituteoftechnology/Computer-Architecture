"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.isRunning = True

        # self.instruction_translate = {
        #     0b00000001: "HLT",
        #     0b10000010: "LDI",
        #     0b01000111: "PRN",
        #     0b10100010: "MUL"
        # }
        # self.instruction_set = {
        #     "HLT": self.HLT,
        #     "LDI": self.LDI,
        #     "PRN": self.PRN,
        #     "MUL": self.MUL
        # }
        self.instruction_set = {
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MUL
        }

    def ram_write(self, val, addy):
        self.ram[addy] = val

    def ram_read(self, addy):
        return self.ram[addy]


    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
        operand_a = 0
        operand_b = 0

        running = True

        while self.isRunning:

            # Grab the bytecode instruction out of memory
            # Use the instruction to access or branch table
            self.instruction_set[self.ram_read(self.pc)]()

    def LDI(self):
        reg_a = self.ram_read(self.pc + 1)
        int = self.ram_read(self.pc + 2)
        self.reg[reg_a] = int
        self.pc += 3
    def MUL(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3
    def PRN(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc += 2
    def HLT(self):
        self.isRunning = False