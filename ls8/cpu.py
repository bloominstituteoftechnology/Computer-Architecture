"""CPU functionality."""

import sys

# opcodes
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101

SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            # Open the file
            with open(sys.argv[1]) as f:
                # Read all the lines
                for line in f:
                    # Parse out the comments
                    comment_split = line.strip().split("#")
                    # Cast number strings to ints
                    value = comment_split[0].strip()
                    # Ignore blank lines
                    if value == "":
                        continue
                    instruction = int(value, 2)
                    # Populate a memory array
                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

    def ram_read(self, mar):
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        # elif op == "SUB": etc
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
        while True:
            opcode = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if opcode == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif opcode == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif opcode == MUL:
                self.alu(opcode, operand_a, operand_b)
                self.pc += 3
            elif opcode == PUSH:
                # Grab the register argument
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]
                # Decrement the SP
                self.reg[SP] -= 1
                # Copy the value in the given register to the address pointed to by the SP.
                self.ram[self.reg[SP]] = val
                self.pc += 2
            elif opcode == POP:
                # Grab the value from the top of the stack
                reg = self.ram[self.pc + 1]
                val = self.ram[self.reg[SP]]
                # Copy the value from the address pointed to by SP to the given register.
                self.reg[reg] = val
                # Increment SP.
                self.reg[SP] += 1
                self.pc += 2
            elif opcode == HLT:
                sys.exit(0)
            else:
                print(f"I did not understand that command: {opcode}")
                sys.exit(1)
