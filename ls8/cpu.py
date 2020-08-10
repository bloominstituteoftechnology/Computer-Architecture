"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # memory
        self.ram = [0] * 256
        # init registers
        self.reg = [0] * 8
        # general-purpose registers
        self.IM = self.reg[5] # interrupt mask
        self.IS = self.reg[6] # interrupt status 
        self.SP = self.reg[7] # stack pointer 
        # special-purpose registers 
        # internal registers
        self.PC = 0 # Program Counter
        self.IR = 0 # Instruction Register
        self.MAR = 0 # Memory Address Register
        self.MDR = 0 # Memory Data Register
        self.FL = 0 # Flags
    
    def ram_read(self, address):
        return self.ram[address] 
    
    def ram_write(self, address, value):
        self.ram[address] = value
 
       
    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = 1
            else:
                self.FL = 0
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        HLT = 0b00000001 # instruction handler
        LDI = 0b10000010 # instruction
        PRN = 0b01000111 # instruction

        if self.ram[self.PC] == LDI:
            self.reg[self.ram[self.PC + 1]] = self.ram[self.PC + 2]
            self.PC += 3

        elif self.ram[self.PC] == PRN:
            print(self.reg[self.ram[self.PC + 1]])
            self.PC += 2    

        elif self.ram[self.PC] == HLT:
            self.PC += 1
            
        