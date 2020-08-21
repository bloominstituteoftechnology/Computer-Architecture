"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
ADD = 0B10100000
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.runnning = True

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("usage: comp.py progname")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.split("#")
                    line = line[0].strip()

                    if line == "":
                        continue
                    else:
                        self.ram[address] = int(line, 2)
                        address += 1
                    
        except FileNotFoundError:
            print(f"Couldn't open {sys.argv[1]}")
            sys.exit(2)

        if address == 0:
            print("Program was empty!")

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, index, value):
        self.ram[index] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB": 
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL": 
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV": 
            self.reg[reg_a] /= self.reg[reg_b]
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

        while self.runnning:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                self.runnning = False
                self.pc += 1
            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif ir == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            elif ir == PUSH:
                self.reg[SP] -= 1
                sp = self.reg[SP]
                value = self.reg[operand_a]
                self.ram[sp] = value
                self.pc += 2
            elif ir == POP:
                sp = self.reg[SP]
                value = self.ram[sp]
                self.reg[operand_a] = value
                self.reg[SP] += 1
                self.pc += 2
            elif ir == CALL:
                self.reg[SP] -=1
                sp = self.reg[SP]
                self.ram[sp] = self.pc + 2
                self.pc = self.reg[operand_a]
            elif ir == RET:
                sp = self.reg[SP]
                self.pc = self.ram[sp]
                self.reg[SP] += 1
            else:
                self.running = False
                print(f"Bad input: {ir}")
                sys.exit(1)