"""CPU functionality."""

import sys

LDI = 0b10000010 # Set a specific register to a specific value
PRN = 0b01000111 # Print a number
HLT = 0b00000001 # Halt the program
MUL = 0b10100010 # Multiply two registers together and store result in register A
POP = 0b01000110 # Pop instruction off the stack
PUSH = 0b01000101 # Push instruction onto the stack
CALL = 0b01010000 # Jump to a subroutine's address
RET = 0b00010001 # Go to return address after subroutine is done

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8
        self.ram = [0] * 255
        self.pc = 0
        self.branchtable = {}
        
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[POP] = self.handle_POP
        self.branchtable[PUSH] = self.handle_PUSH

        self.register[7] = 0xF4 # initialized to point at key press

    def handle_POP(self):
        SP = self.register[7]
        value = self.ram[SP]
        reg = self.ram_read(self.pc + 1)
        self.register[reg] = value
        self.register[7] += 1
        self.pc += 2

    def handle_PUSH(self):
        self.register[7] -= 1
        SP = self.register[7]
        reg = self.ram_read(self.pc + 1)
        self.ram_write(self.register[reg], SP)
        self.pc += 2



    def handle_LDI(self):
        reg = self.ram_read(self.pc + 1)
        num = self.ram_read(self.pc + 2)
        self.register[reg] = num
        self.pc += 3

    def handle_PRN(self):
        reg = self.ram_read(self.pc + 1)
        num = self.register[reg]
        print(num)
        self.pc += 2

    def handle_HLT(self):
        sys.exit(1)

    def handle_MUL(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3

    def load(self):
        """Load a program into memory."""
        path = sys.argv[1]

        address = 0

        with open(path) as file:
            for line in file:
                if line[0] != "#" and line !='\n':
                    self.ram[address] = int(line[:8], 2)
                    address += 1
        # print(self.ram)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
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
        
        while True:
            IR = self.ram[self.pc]
            self.branchtable[IR]()

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR
