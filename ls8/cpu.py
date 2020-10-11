"""CPU functionality."""

import sys
from table import Branchtable

class CPU:
    """Main CPU class."""

    def __init__(self, program):
        """Construct a new CPU."""
        # Clear Registers
        self.reg = [0] * 8
        
        # set internal registers to 0
        self.pc = 0
        self.ir = 0
        self.fl = 0
        self.mar = 0
        self.mdr = 0

        # initialize stack pointer
        self.sp = 0xF4

        # RAM is cleared to zero
        self.ram = [0] * 256

        # R7 is set to keyboard interupt
        self.reg[7] = self.ram[0xF4]

        # set halt flag
        self.halt = False

        # load program into memory
        self.load(program)

        # initialize branchtable
        self.branchtable = Branchtable(self)

    def load(self, program):
        """Load a program into memory."""

        address = 0
        data = []

        # parse program all lines in the file
        with open(program, 'r') as f:
            for line in f:
                # check for comments
                line = line.split('#')[0]

                # remove new line tokens
                line = line.strip('\n') 

                # check for empty lines
                if line:
                    data.append(int(line, 2))        

        for instruction in data:
            self.ram_write(address, instruction)
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            if reg_b == 0:
                raise Exception("Can't divide by zero")
                # halt program
                self.halt = True
            
            self.reg[reg_a] /= self.reg[reg_b]
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
        '''
        read data at provided address and return value stored there
        '''
        # store current memory address being read
        self.mar = mar

        # store data retrieved from that address
        self.mdr = self.ram[mar]

        return self.mdr
    
    def ram_write(self, mar, mdr):
        '''
        write provided data to provided memory location in RAM
        '''
        # store memory address being written to
        self.mar = mar

        # store data loaded at that address
        self.mdr = mdr

        # store data in ram
        self.ram[mar] = mdr

    def run(self):
        """Run the CPU."""
        while not self.halt:
            # load instruction register
            self.ir = self.ram_read(self.pc)

            # get operands
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]

            # get instruction from table
            if self.branchtable.contains(self.ir):
                instruction = self.branchtable.instruction(self.ir)

            # run the routine
            instruction(operand_a, operand_b)

            # check if program counter is manually set
            if (self.ir >> 4) & 0b0001 == 1:
                continue
            else:
                # increment program counter adding in num of operands needed
                self.pc += 1 + (self.ir >> 6)
            

            



        

        
