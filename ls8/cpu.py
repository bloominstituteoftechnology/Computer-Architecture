"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
    #  Add list properties to the `CPU` class to hold 256 bytes of memory
    # and 8 general-purpose registers.
        self.ram = [0] * 256  # memory is a list of 256 zeroes
        self.register = [0] * 8  # 8 registers
        self.pc = 0  # Program Counter, points to currently-executing instruction

    # In `CPU`, add method `ram_read()` and `ram_write()`
    # that access the RAM inside the `CPU` object.

    """`ram_read()` should accept the address to read and return the value stored there."""

    def ram_read(self, address):
        return self.ram[address]

    """`ram_write()` should accept a value to write, and the address to write it to."""

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, argv):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        try:
            # sys.argv is a list in Python, which contains the command-line arguments passed to the script.
            with open(sys.argv[1]) as f:  # open a file
                for line in f:
                    if line[0].startswith('0') or line[0].startswith('1'):
                        # search first part of instruction
                        num = line.split('#')[0]
                        num = num.strip()  # remove empty space
                        # convert binary to int and store in a memory(RAM)
                        self.ram[address] = int(num, 2)
                        address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} Not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            # self.reg[reg_a] += self.reg[reg_b]
            self.register[reg_a] += self.register[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
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

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010

        running = True

        while running:
            # It needs to read the memory address that's stored in register `PC`,
            # and store that result in `IR`, the _Instruction Register_.
            # This can just be a local variable in `run()`.
            IR = self.ram[self.pc]

            # Using `ram_read()`, read the bytes at `PC+1` and `PC+2` from RAM into variables
            # `operand_a` and `operand_b` in case the instruction needs them.
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # Decoding
            if IR == LDI:
                self.register[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                print(self.register[operand_a])
                self.pc += 2
            elif IR == HLT:
                running = False
            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            else:
                print(f"Unknown instruction!!{self.ram[self.pc]} ")
                sys.exit(1)


# RUN in terminal as:-----------------
# python3 ls8.py examples/print8.ls8
# prints: 8
# python3 ls8.py examples/mult.ls8
# prints: 72
# --------------------------------------
