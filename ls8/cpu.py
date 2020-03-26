"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self, filename):
        """Construct a new CPU."""
        self.reg = [0] * 256
        self.ram = [0] * 16
        self.filename = filename
    def load(self):
        """Load a program into memory."""

        address = 0

        with open(self.filename, 'r') as f:
            program = f.read().splitlines()
            program = ['0b'+line[:8] for line in program if line and line[0] in ['0', '1']]


        for instruction in program:
            self.ram[address] = eval(instruction)
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

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

        address = 0
        while address < len(self.ram) - 1:
            instruction = self.ram[address]
            # LDI
            if instruction == 0b10000010:
                register = self.ram[address + 1]
                integer = self.ram[address + 2]
                address += 3
                self.reg[register] = integer
            # PRN
            elif instruction == 0b01000111:
                register = self.ram[address + 1]
                address += 2
                print(self.reg[register])
            elif instruction == 0b10100010:
                self.alu("MUL", self.ram[address + 1], self.ram[address + 2])
                address += 3
            # HLT
            elif instruction == 0b00000001:
                break






            else:
                raise TypeError("That command has not been implemented yet")
