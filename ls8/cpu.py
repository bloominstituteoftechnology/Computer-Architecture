"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def ram_read(self, MAR):
        # Memory Address Register (MAR)
        # MAR contains the address that is being read
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        # MDR contains the data that was read or the data to write.
        # Memory Data Register (MDR)
        # Memory Address Register (MAR)
        # MAR contains the address that is being read or written to
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        print(sys.argv)

        if len(sys.argv) != 2:
            print('Usage: ls8.py filename')
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    split_line = line.split('#')

                    value = split_line[0].strip()

                    if value == '':
                        continue

                    instruction = int(value, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print(f'{sys.argv[1]} file not found')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc

        elif op == "MUL":
            sum = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = sum
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010

        running = True

        while running:
            instruction = self.ram[self.pc]
            if instruction == LDI:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif instruction == PRN:
                operand_c = self.ram_read(self.pc + 1)
                print(self.reg[operand_c])
                self.pc += 2
            elif instruction == HLT:
                running = False
            elif instruction == MUL:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.alu('MUL', reg_a, reg_b)
                self.pc += 3
