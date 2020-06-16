"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        for instruction in program:
            self.ram[address] = instruction
            # print(f"i am an instruction: {self.ram[address]}")
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc\
        elif op == "MUL":
            #accept instruction
            #write to reg_a
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        # accept address
        # return it's value
        return self.ram[address]

    def ram_write(self, value, address):
        # take a value
        # write to address
        # no return
        self.ram[address] = value


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
        
        running = True
        while running:
            ir = self.ram[self.pc]

            if ir == self.LDI:
                self.ldi()

            elif ir == self.PRN:
                self.prn()

            elif ir == self.HLT:
                running = self.hlt()
            elif ir == self.MUL:
                running = self.mult()


    def ldi(self):
        address = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.reg[address] = value
        self.pc += 3

    def prn(self):
        address = self.ram[self.pc + 1]
        value = self.reg[address]
        print(value)
        self.pc += 2

    def hlt(self):
        self.pc += 1
        return False

    def mult(self):
        # a = self.ram[self.pc + 1]
        # b = self.ram[self.pc + 2]
        self.alu("MUL", 0, 1)
        print(f'RAM: {self.ram}')
        print(f'Reg: {self.reg}')
        self.pc += 3
