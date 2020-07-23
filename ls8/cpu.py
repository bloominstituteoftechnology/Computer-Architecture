"""CPU functionality."""

import sys

HTL = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

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

        self.branch_table = {}
        self.branch_table[HTL] = self.hlt_inst
        self.branch_table[LDI] = self.ldi_inst
        self.branch_table[PRN] = self.prn_inst
        self.branch_table[MUL] = self.mul_inst

    def ram_read(self, MAR):
        if MAR < len(self.ram):
            return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        if MAR < len(self.ram):
            self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""
        while True:
            # inst = bin(self.ram[self.pc])
            IR = self.ram_read(self.pc)
            self.branch_table[IR]()


    def hlt_inst(self):
        exit(1)

    def mul_inst(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)

        result = self.reg[reg_a] * self.reg[reg_b]
        self.reg[reg_a] = result
        self.pc += 3

    def ldi_inst(self):
        MAR = self.ram_read(self.pc + 1)
        MDR = self.ram_read(self.pc + 2)
        if MAR < len(self.ram):
            self.reg[MAR] = MDR
        self.pc += 3

    def prn_inst(self):
        operand_a = self.ram_read(self.pc + 1)
        print(self.reg[operand_a])
        self.pc += 2

    def load(self, file):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("usage: comp.py filename")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    try:
                        line = line.split("#", 1)[0]
                        line = int(line, 2)
                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass

        except FileNotFoundError:
            print(f"Couldn't find file {sys.argv[1]}")
            sys.exit(1)

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
        #
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        # print(self.ram)

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
