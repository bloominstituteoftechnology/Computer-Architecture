"""CPU functionality."""

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

    def ram_read(self, count):
        return self.ram[count]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        self.load()

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        IR = self.pc
        operand_a = self.ram_read(IR+1)
        operand_b = self.ram_read(IR+2)
        running = True

        while running:

            if self.ram[IR] == LDI:
                #load operand_b into ram at location ram[operand_a]
                self.ram_write(operand_a, operand_b)
                #increment the IR by two
                IR += 3
                print(f"ram loaded with the value: {self.ram[operand_a]}")

            elif self.ram[IR] == PRN:
                #print the thing and increment.
                print(f"you requested a print?  {self.ram[self.ram[IR+1]]}")
                IR += 2

            elif self.ram[IR] == HLT:
                running = False
                print(f"no longer running. buhbye now.")
            else:
                print(f"unrecognized input, moving to next cycle")
                IR += 1 
        
