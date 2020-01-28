"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of memory
        self.register = [0] * 8
        self.ram = [0] * 255
        # Program Counter, address of the currently executing instruction
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

    def run(self):
        """Run the CPU."""
        # Memory address that's stored in register PC

        running = True

        while running:
            IR = self.pc
            program = self.ram_read(self.pc)
            registerA = self.ram_read(self.pc + 1)
            registerB = self.ram_read(self.pc + 2)
            # Execute instructions in memory

            # HLT - Halts running
            if program == 0b00000001:
                running = False

            # LDI - sets value of register to INT
            if program == 0b10000010:
                # convert to int, base 2
                registerInt = int(str(registerA), 2)
                self.register[registerInt] = registerB
                self.pc += 3

            # PRN - Print numeric value stored in register
            if program == 0b01000111:
                print(self.register[int(str(registerA))])
                self.pc += 2

    def ram_read(self, address):
        """Accepts an address to read,
        and return the value stored there."""
        # if address in ram:
        return self.ram[address]
        # else:
        #     raise Exception("Address does not exist!")

    def ram_write(self, address, value):
        """Accepts a value to write,
        and the address to write it to."""
        self.ram[address] = value
