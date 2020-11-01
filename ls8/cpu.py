"""CPU functionality."""
import os
import sys

from examples import *

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 8
        self.running = True
        self.registers = {}

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

    def ram_read(self,val):
        print(self.ram[val])
    
    def ram_write(self, val, address):
        self.ram[address] = val

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")


    def load_memory(self): 
        if len(sys.argv) != 2:
            print("Usage cpu.py filename.ls8")
            sys.exit(1)

        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    split_line = line.split('#')
                    cleaned = split_line[0].strip()

                    if cleaned == '':
                        continue
                    try:
                        cleaned = int(cleaned, 2)
                    except ValueError:
                        print(f'{cleaned} is not a valid value')
                        sys.exit(1) 

                    self.ram_write(address, cleaned)
                    address +=1

        except FileNotFoundError:
            print(f'{filename} does not exist')
            sys.exit(2)

        # print("Usage: enter in a filename....")



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
        
        print(self.ram)
        pc = 0
        while self.running:
            instruction = self.ram[pc]
            if instruction == 130: #op code 130 is LDI
                index = self.ram[pc +1]
                val = self.ram[pc+2]
                self.registers[index] = val
                pc += 3
            elif instruction == 71:
                reg_choice = self.ram[pc+1] #gives a number
                val = self.registers[reg_choice]
                print(val)
                pc +=1
            elif instruction ==1:
                self.running = False
            else:
                self.running = False


# c = CPU()
# c.load_memory(sys.argv[1])
