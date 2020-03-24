"""CPU functionality."""

#hlt halts the program
#ldi load immediate
#prn print
#load "immediate", store a value in a register, or "set this register to this value"

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

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
    def ram_read(self, mar):
        #memory address registry mar, this might as well be the index
        #memory data register mdr
        #cpu register --> fixed small number of special storage locations built in
        #hexadecimal leading 0x binary leading 0b
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr



    def run(self):
        """Run the CPU."""
        pc = 0 
        IR = None

        running = True
        self.load()
        while running:
            if self.ram[pc] == 130:
                self.reg[self.ram[pc+1]] = self.ram[pc+2]
                pc += 3
            elif self.ram[pc] == 71:
                print(self.reg[self.ram[pc+1]])
                pc += 2
            elif self.ram[pc] == 1:
                running = False
            
            # command = memory[pc]

pc = CPU()
pc.run()
