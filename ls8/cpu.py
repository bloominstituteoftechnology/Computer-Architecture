"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MULT = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
SP = 7  # stack pointer is reg7
ADD = 0b10100000
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JEQ = 0b01010101
JMP = 0b01010100
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        self.pc = 0
        self.halted = False
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4  # stack pointer
        self.less = 0
        self.greater = 0
        self.equal = 0

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, val, address):
        self.ram[address] = val

    def load(self):
        """Load a program into memory."""
        address = 0
        with open(sys.argv[1]) as fp:
            for line in fp:
                comment_split = line.split("#")
                num = comment_split[0].strip()
                if num == "":
                    continue
                value = int(num, 2)  # set value to the number (of base 2)
                self.ram_write(value, address)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":  # add
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MULT":  # multiply
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":  # compare
            if self.reg[reg_a] < self.reg[reg_b]:
                self.less = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.greater = 1
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.equal = 1
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
            instruction = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.execute_instruction(instruction, operand_a, operand_b)

    def execute_instruction(self, instruction, operand_a, operand_b):
        if instruction is LDI:
            self.reg[operand_a] = operand_b
            self.pc += 3

        elif instruction is PRN:
            print(self.reg[operand_a])
            self.pc += 2

        elif instruction is ADD:
            self.alu("ADD", operand_a, operand_b)
            self.pc += 3

        elif instruction is MULT:
            self.alu("MULT", operand_a, operand_b)
            self.pc += 3

        elif instruction is CMP:
            self.alu("CMP", operand_a, operand_b)
            self.pc += 3

        elif instruction is POP:
            self.reg[operand_a] = self.ram[self.reg[SP]]
            self.reg[SP] += 1
            self.pc += 2

        elif instruction is PUSH:
            self.reg[SP] -= 1
            self.ram[self.reg[SP]] = self.reg[operand_a]
            self.pc += 2

        elif instruction is CALL:
            self.reg[self.reg[SP]] -= 1
            self.ram[self.reg[SP]] = self.pc + 2
            self.pc = self.reg[operand_a]

        elif instruction is RET:
            self.pc = self.ram[self.reg[SP]]
            self.reg[self.reg[SP]] += 1

        elif instruction is JMP:
            self.pc = self.reg[operand_a]

        elif instruction is JEQ:
            if self.equal == 1:
                self.pc = self.reg[operand_a]
            else:
                self.pc += 2

        elif instruction is JNE:
            if self.equal == 0:
                self.pc = self.reg[operand_a]
            else:
                self.pc += 2

        elif instruction is HLT:
            self.halted = True

        else:
            print("Idk this instruction, exiting.")
            sys.exit(1)
