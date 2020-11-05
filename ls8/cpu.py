"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MULT = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.halted = False
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4

    def load(self, filename):
        """Load a program into memory."""
        address = 0
        with open(filename) as fp:
            for line in fp:
                comment_split = line.split("#")
                num = comment_split[0].strip()
                if num == '': 
                    continue
                val = int(num, 2)
                self.ram_write(val, address)
                address += 1

    def ram_write(self, value, address):
        self.ram[address] = value

    def ram_read(self, address):
        return self.ram[address]

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
        while not self.halted:
            # self.trace()
            instruction_to_execute = self.ram[self.pc]
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]
            self.execute_instruction(instruction_to_execute, operand_a, operand_b)

    def execute_instruction(self, instruction, operand_a, operand_b):
        if instruction == HLT:
            self.halted = True
            self.pc += 1
        elif instruction == PRN:
            print(self.reg[operand_a])
            self.pc += 2
        elif instruction == LDI:
            self.reg[operand_a] = operand_b
            self.pc += 3
        elif instruction == MULT:
            self.reg[operand_a] *= self.reg[operand_b]
            self.pc += 3
        elif instruction == PUSH:
            self.reg[SP] -= 1
            valueFromRegister = self.reg[operand_a]
            self.ram_write(valueFromRegister, self.reg[SP])
            self.pc += 2
        elif instruction == POP:
            topmostValue = self.ram_read(self.reg[SP])
            self.reg[operand_a] = topmostValue
            self.reg[SP] += 1
            self.pc += 2
        else:
            print("quit")
            sys.exit(1)