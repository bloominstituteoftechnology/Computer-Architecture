"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #self.ram = {}
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8  ----130?
            0b00000000,
            0b00001000, #8
            0b01000111, # PRN R0 ---71
            0b00000000,
            0b00000001, # HLT ----1
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

        

    


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

    def ram_read(self):
        index = self.ram[self.pc + 1]
        print(self.reg[index])

    
    def ram_write(self, operand_a,operand_b):
        self.reg[operand_a] = operand_b    

    
    def run(self):
        self.running = True
        while self.running:
            command = self.ram[self.pc]
            if command == HLT:
                self.running = False
                self.pc = 0
            if command == PRN:
                self.ram_read()
                self.pc += 2
            if command == LDI:
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
                self.ram_write(operand_a, operand_b)
                self.pc += 3


            # else:
            #     print(f"Unknown instruction at index {self.pc}")
            #     print(self.reg)
            #     print(self.ram)
                
            #     sys.exit(1)


            