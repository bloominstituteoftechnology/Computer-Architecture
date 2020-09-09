"""CPU functionality."""

import os.path
from os import path

import sys


class CPU:
    """Main CPU class."""

    ## NOT SURE WHAT TO DO ABOUT LISTING INVENTORY ##

    def __init__(self):
        """Construct a new CPU."""
        self.ram = {}
        self.registers = [0] * 8
        

    def load(self):
        """Load a program into memory."""

        file_name = sys.argv[1]

        program = []

        f = open(file_name, "r")

        for line in f:

            program.append(line[:8])

        f.close()

        print("Program from Load: ", program)

        address = 0

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

    def run(self):
        """Run the CPU."""
        
        running = True

        pc = 0


        while running:
            # Read Line by Line from Memory
            instruction = self.ram[pc]

            if instruction == '10000010':
                
                reg_location = self.ram[pc + 1]

                num = self.ram[pc + 2]

                self.registers[int(reg_location)] = num

                pc += 3

            elif instruction == '01000111':

                reg_location = self.ram[pc + 1]

                print(self.registers[int(reg_location)])

                pc += 2

            elif instruction == '00000001':

                running = False

                pc += 1
            
            elif instruction == '10100010':

                print("BICHO")

                reg_location_1 = self.ram[pc + 1]

                reg_location_2 = self.ram[pc + 2]

                ## Multiply Numbers Here ##

                pc += 3
        
            else: 
                
                print(f"Unknown Instruction: {instruction}")

                sys.exit(1) 
