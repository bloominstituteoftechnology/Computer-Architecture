"""CPU functionality."""

import sys
from ls8Instructions import *


IM = 5 # Interrupt Mask Index
IS = 6 # Interrupt Status Index
SP = 7 # Stack Pointer Index
    
class CPU:
    """Main CPU class."""
    

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # RAM capacity of 256 bytes
        self.ir = [0] * 8 # Setting up 8 general-purpose resgisters
        self.pc = 0 # Program Counter
        self.flags = 0
        self.ir[SP] = 0xF4


    def load(self, program_filepath):
        """Load a program into memory."""

        address = 0

        with open(program_filepath) as f:
            for line in f:
                line = line.split("#")
                line = line[0].strip()
        
                if line == '':
                    continue
                # line = int(line) # For the daily project we want int(line, 2) <- saying we want base 2 for binary
                self.ram[address] = int(line, 2)
        
                address += 1
            
    
    def ram_read(self, MAR):
        return self.ram[MAR]
    
    
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR


    def alu(self, op, reg_a, reg_b):
        
        """ALU operations."""

        if op == "ADD":
            self.ir[reg_a] += self.ir[reg_b]
        elif op == "MULT":
            self.ir[reg_a] *= self.ir[reg_b]
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
            print(" %02X" % self.ir[i], end='')

        print()
        
        
    def handle_hlt(self, hlt):
        exit()
        
    def handle_ldi(self, ldi):
        reg_num = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.ir[reg_num] = value
        self.pc += 3

    def run(self):
        """Run the CPU."""
        while True:
            inst = self.ram_read(self.pc)
            self.trace()
            # print("Instruction: ", hex(inst))
            if inst == HLT:
                exit()
            elif inst == LDI:
                reg_num = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc + 2)
                self.ir[reg_num] = value
                self.pc += 3
            elif inst == PRN:
                reg_num = self.ram_read(self.pc + 1)
                value = self.ir[reg_num]
                print(value)
                self.pc += 2
            elif inst == MUL:
                reg_numA = self.ram_read(self.pc + 1)
                reg_numB = self.ram_read(self.pc + 2)
                self.alu("MULT", reg_numA, reg_numB)
                self.pc += 3
            elif inst == PUSH:
                self.ir[SP] -= 1
                reg_num = self.ram_read(self.pc + 1)
                value = self.ir[reg_num]
                address = self.ir[SP]
                self.ram_write(address, value)
                self.pc += 2
            elif inst == POP:
                reg_num = self.ram_read(self.pc + 1)
                address = self.ir[SP]
                value = self.ram[address]
                self.ir[reg_num] = value
                self.ir[SP] += 1
                self.pc += 2
            else:
                print("Unknown Instruction: ", hex(inst))
                exit()
            
