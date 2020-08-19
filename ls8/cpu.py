"""CPU functionality."""

import time
import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg_pc = 0

    def ram_read(self, pos):
        return self.ram[pos]

    def ram_write(self, value, pos):
        self.ram[pos] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("Program requires second system argument to run.")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    temp = line.split()
                    if len(temp) == 0 or temp[0][0] == "#":
                        continue

                    try:
                        self.ram[address] = int(temp[0], 2)

                    except ValueError:
                        print(f"Invalid value: {int(temp[0], 2)}")

                    address += 1


        except FileNotFoundError:
            print(f"Couldn't open {sys.argv[1]}")
            sys.exit(2)

        if address == 0:
            print("Program is empty!")
            sys.exit(3)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]

        elif op == "DIV":
            self.reg[reg_a] = self.reg[reg_a] / self.reg[reg_b]
     
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

    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:

            # Ensures we won't need to restart Anaconda Prompt
            # every time that something goes wrong.
            start = time.time()
            if time.time() - start > 0.5:
                return

            # LDI - sets value of register to integer
            if self.ram_read(self.pc) == 0b10000010:
                self.reg[self.reg_pc] = self.ram_read(self.pc + 2)
                self.reg_pc += 1

                self.pc += 3

            # PRN, R0
            if self.ram_read(self.pc) == 0b01000111:
                print(self.reg[0])

                self.pc += 2

            # HALT
            if self.ram_read(self.pc) == 0b00000001:
                break

            if self.ram_read(self.pc) == 0b10100010:
                self.alu("MUL", 0, 1)

                self.pc += 3

