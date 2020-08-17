"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.running = True
        self.pc = 0

    def ram_read(self, MAR):
        """
        Accepts the address to read and returns the value stored
        there.

        Input: MAR: _Memory Address Register_ ... address to read
        """
        if MAR < len(self.ram) - 1:
            return self.ram[MAR]

        else:
            return "INDEX ERROR: Requested address out of memory range."

    
    def ram_write(self, MDR, MAR):
        """
        Accepts a value to write, and the address to write it to.

        Inputs: MAR: _Memory Address Register_ ... address to write to
                MDR: _Memory Data Register_ ... data to write
        """
        self.ram[MAR] = MDR


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

        # Using binary codes
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        while self.running:

            # HLT Instruction - aka halt, stop running
            if self.ram[self.pc] == HLT:
                self.running = False
            
            # LDI Instruction - Set the value of a register to an integer.
            if self.ram[self.pc] == LDI:
                num_to_load = self.ram[self.pc + 2]
                reg_index = self.ram[self.pc + 1]
                self.reg[reg_index] = num_to_load
                self.pc += 3
            
            # PRN Instruction -Print numeric value stored in the given register. 
            # Print to the console the decimal integer value that is stored in the given register.
            if self.ram[self.pc] == PRN:
                reg_to_print = self.ram[self.pc + 1]
                print(self.reg[reg_to_print])
                self.pc += 2


if __name__ == "__main__":
    
    
    cpu = CPU()

    print("Before write:", cpu.ram_read(250))

    cpu.ram_write(3, 250)

    print("After write:", cpu.ram_read(250))