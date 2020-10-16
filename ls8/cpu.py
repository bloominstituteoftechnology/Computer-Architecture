"""CPU functionality."""

import sys

CMP = 0b10100111
JMP = 0b01010100 
JEQ = 0b01010101
JNE = 0b01010110  


class CPU:
    """Main CPU class."""


    def __init__(self):
        """Construct a new CPU."""
        self.list = [0] * 25 # list of 25 zeros
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.flag = 0b00000000

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
        return self.ram[address]
      

    def load(self):
        """Load a program into memory."""
        if len(sys.argv) < 2:
            print("usage: comp.py filename")
            sys.exit(1)

        address = 0
        
        with open(sys.argv[1]) as f:
            for line in f:
                string_val = line.split("#")[0].strip()

                if string_val == "":
                    continue
                v = int(string_val, 2)
                self.ram[address] = v
                adress += 1

            # except FileNotFoundError:
            #     print(f"Couldn't find file {sys.argv[1]}")
            #     sys.exit(1)

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

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

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
        while True:
            IR = self.ram_read(self.pc)

            a = self.ram_read(self.pc + 1)
            b = self.ram_read(self.pc + 2)

            if IR == CMP:
                if self.reg[a] == self.reg[b]:
                    self.flag = 0b00000001
                else:
                    self.flag = 0b00000000
                if self.reg[a] < self.reg[b]:
                    self.flag = 0b00000100
                else:
                    self.flag = 0b00000000
                if self.reg[a] > self.reg[b]:
                    self.flag = 0b00000010
                else:
                    self.flag = 0b00000000
                self.pc += 3
            elif IR == JMP:
                self.pc == self.reg[a]
            
            elif IR == JNE:
                if self.flag != 0b00000001:
                    self.pc = self.reg[a]
                else:
                    self.pc += 2

            elif IR == JEQ:
                if self.flag == 0b00000001:
                    self.pc = self.reg[a]
                else:
                    self.pc += 2
        
        


    
