"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # We need 256 bytes of Ram, 8 registers, a counter, and continuous variable
        self.ram = [None] * 256
        self.registers = [None] * 8
        self.running = True
        self.pc = 0

    def ram_read(self, address):
        # Accepts the address and returns the value from Ram
        return(self.ram[address])    

    def ram_write(self, value, address):
        # Accepts a value and address and assigns to Ram
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
            self.registers[reg_a] += self.registers[reg_b]
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
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        while self.running:
            # The HLT instruction
            if self.ram[self.pc] == HLT:
                self.running = False
            
            # The LDI instruction
            if self.ram[self.pc] == LDI:
                num_to_load = self.ram[self.pc + 2]
                reg_index = self.ram[self.pc + 1]
                self.registers[reg_index] = num_to_load
                self.pc += 3
            
            # The PRN instruction
            if self.ram[self.pc] == PRN:
                reg_to_print = self.ram[self.pc + 1]
                print(self.registers[reg_to_print])
                self.pc += 2
