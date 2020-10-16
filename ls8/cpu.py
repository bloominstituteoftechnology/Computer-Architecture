"""CPU functionality."""

import sys
import re

CMP = 0b10100111
JMP = 0b01010100 
JEQ = 0b01010101
JNE = 0b01010110  


class CPU:
    """Main CPU class."""


    def __init__(self):
        """Construct a new CPU."""
        self.instruction_list = {}  #A dict to hold current instructions
        self.list = [0] * 25 # list of 25 zeros
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8


        self.E = None #Equal To
        self.L = None #Less than
        self.G = None # Greater than


        self.instruction_list[CMP] = self.cmp_inst
        self.instruction_list[JMP] = self.jmp_inst
        self.instruction_list[JEQ] = self.jeq_inst

    def ram_read(self, adress):
        if adress < len(self.ram):
            return self.ram[adress]

    def ram_write(self, adress, value):
        if adress < len(self.ram):
            self.ram[adress] = value

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

    def jmp_inst(self):
        a = self.ram_read(self.pc + 1)
        self.pc = self.reg[a]

    def jeq_inst(self):
        if self.E == 1:
            self.jmp_inst()
        else:
            self.pc += 2
    
    def cmp_inst(self):
        a = self.ram_read(self.pc + 1)
        b = self.ram_read(self.pc + 2)

        if self.reg[a] == self.reg[b]:
            self.E = 1
        else:
            self.E = 0
        
        if self.reg[a] < self.reg[b]:
            self.L = 1
        else:
            self.L = 0
            
        if self.reg[a] > self.reg[b]:
            self.G = 1
        else:
            self.G = 0

        self.pc += 3
    
    def jne_inst(self):
        if self.E == 0:
            self.jmp_inst()
        else:
            self.pc += 2

    def run(self):
        """Run the CPU."""
        while True:
            IR = self.ram_read(self.pc)

            if IR in self.instruction_list:
                self.instruction_list[IR]()

            else:
                print(f"Errow with instruction at: {IR}", IR)
        


    
