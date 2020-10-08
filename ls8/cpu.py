"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.ir = 0
        self.mar = 0
        self.mdr = 0
        self.halted = False
        self.sp = 7

        self.reg[7] = 0xF4

        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP

    def ram_read(self, mar):
        return self.ram[mar]
    
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr


    def load(self):
        """Load a program into memory."""
        if (len(sys.argv)) != 2:
            print("Remember to pass the second file name")
            print("Usage: python3 ls8.py <second_file_name.py>")
            sys.exit()

        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    split = line.split("#")
                    value = split[0].strip()
                    if value == "":
                        continue
                    
                    try:
                        instruction = int(value, 2)
                    except ValueError:
                        print(f'Invalid number {value}')
                        sys.exit(1)
                    
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
            sys.exit()

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
        while not self.halted:
            self.ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if not ((self.ir >> 4) & 0b0001) == 1:
                self.pc += ((self.ir >> 6) & 0b11) + 1

            self.handle_instruction(operand_a, operand_b)

    def handle_instruction(self, operand_a, operand_b):
        if self.ir in self.branchtable:
            self.branchtable[self.ir](operand_a, operand_b)
        else:
            print(f"Error: Could not find instruction: {self.ir} in branch table.")
            sys.exit(1)

    def handle_HLT(self, a=None, b=None):
        self.halted = True

    def handle_LDI(self, num, val):
        self.reg[num] = val

    def handle_PRN(self, num, b=None):
        print(self.reg[num])

    def handle_MUL(self, num, num2):
        self.reg[num] = self.reg[num] * self.reg[num2]

    def handle_PUSH(self, num, b=None):
        self.sp -= 1
        self.mdr = self.reg[num]
        self.ram_write(self.sp, self.mdr)

    def handle_POP(self, num, b=None):
        self.mdr = self.ram_read(self.sp)
        self.reg[num] = self.mdr
        self.sp += 1