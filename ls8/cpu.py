"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Set up the branch table
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        
    def ram_read(self, mar):
        print(self.reg[mar])
        return self.reg[mar]

    def ram_write(self, mar, mdr):
        self.reg[mar] = mdr

    def load(self):
        """Load a program into memory."""
        try:
            address = 0
            with open(sys.argv[1]) as f:
                # Read all the lines
                for line in f:
                    comment_split = line.strip().split("#")
                    # Cast the number from string to ints
                    value = comment_split[0].strip()
                    self.ram[address] = int(value,2)
                    address += 1
            print(self.ram)
        except FileNotFoundError:
            print("File not Found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            result = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = result
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

    def handle_LDI(self):
        self.ram_write(self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def handle_PRN(self):
        self.ram_read(self.ram[self.pc + 1])
        self.pc += 2

    def handle_MUL(self):
        self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3


    def run(self):
        while True:
            IR = self.ram[self.pc]
            if IR == HLT:
                exit(2)
            self.branchtable[IR]()

