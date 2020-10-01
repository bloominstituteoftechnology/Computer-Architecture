"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.registers = [0] * 8
        self.ram = [0b00000000] * 256

    @property
    def pc(self):
        '''Returns the Program Counter, address of currently executing
        instruction'''
        return self.registers[0]

    @property
    def ir(self):
        '''Instruction Register, contains copy of currently executing 
        instruction'''
        return self.registers[1]

    @property
    def mar(self):
        '''Memory Address Register, holds the memory address being read or 
        written to.'''
        return self.registers[2]

    @property
    def mdr(self):
        '''Memory Data Register, holds the value to write or the value read'''
        return self.registers[3]

    @property
    def fl(self):
        '''Flags register'''
        pass


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
        pass
