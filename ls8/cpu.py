"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        register = [0] * 8
        memory = [0] * 256
        pc = []
        # This is a flag
        fl = 0b0000
        # This flag is used to indicate less-than
        l = 0
        # This flag is used to indicate greater-than
        g = 0
        # This flag is used to indicate equality between values
        e = 0
        # This is temporary memory
        stack = []
        # This is the instruction register, it contains a copy of the currently executing instruction
        ir = []
        if len(stack) > 0:
            # This is the stack pointer. It points to the top item of the stack. If there is not a top item of the stack, it points to 0xF4, which is the address in memory that stores the most recently pressed key.
            sp = stack[0]
        else:
            sp = memory[0xF4]

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

    def ram_read(self, address):
        return self.memory[address]
    
    def ram_write(self, address, value):
        self.memory[address] = value
    

    def run(self):
        """Run the CPU."""
        pass
