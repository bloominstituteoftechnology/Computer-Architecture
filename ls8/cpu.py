"""CPU functionality."""

import sys

LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
MUL = 0b10100010
NOP = 0b00000000

class CPU:
    """Main CPU class."""
    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True

    def load(self):
        filename = sys.argv[1]

        with open(filename) as f:
            for address, line in enumerate(f):
                line = line.split('#')
                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue
                self.ram_write(address, v)


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

    def LDI(self):
        reg_num = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[reg_num] = value
        self.pc += 3

    def HLT(self):
        self.running = False
    
    def PRN(self):
        reg_num = self.ram_read(self.pc + 1)
        print(self.reg[reg_num])
        self.pc += 2
    
    def MUL(self):
        reg_num1 = self.ram_read(self.pc + 1)
        reg_num2 = self.ram_read(self.pc + 2)
        self.alu("MUL", reg_num1, reg_num2)
        self.pc += 3

    def NOP(self):
        self.pc += 1

    def call_fun(self, n):
        branch_table = {
            NOP : self.NOP,
            HLT : self.HLT,
            PRN : self.PRN,
            LDI : self.LDI,
            MUL : self.MUL
        }

        f = branch_table[n]
        if branch_table.get(n) is not None:
            f()
        else:
            print(f'Unknown instruction {n} at address {self.pc}')
            sys.exit(1)

    def run(self):
        while self.running:
            ir = self.ram_read(self.pc)
            self.call_fun(ir)
            

    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, address, value):
        self.ram[address] = value
