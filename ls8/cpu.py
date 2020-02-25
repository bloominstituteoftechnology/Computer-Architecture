"""CPU functionality."""

from ls8Instructions import *
import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.register[7] = 0xF4

        self.pc = 0
        self.fl = 0

    def load(self, program):
        """Load a program into memory."""

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ramRead(self, mar):
        return self.ram[mar]

    def ramWrite(self, mdr, mar):
        self.ram[mar] = mdr

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

        while True:
            instructionRegister = self.ram[self.pc]

            if instructionRegister == LDI:
                operandA = self.ram[self.pc + 1]
                operandB = self.ram[self.pc + 2]
                self.register[operandA] = operandB
            elif instructionRegister == PRN:
                operandA = self.ram[self.pc + 1]
                value = self.register[operandA]
                print(value)
            elif instructionRegister == MUL:
                operandA = self.ram[self.pc + 1]
                operandB = self.ram[self.pc + 2]
                self.register[operandA] = self.register[operandA] * self.register[operandB]
            elif instructionRegister == HLT:
                exit(0)
            else:
                print(f"Instruction not recognized: {instructionRegister}")
                exit(1)

            # offset pc by whatever the previous register said to offset by (MIGHT be problematic here, but for now is DRY)
            self.pc += ((instructionRegister & 0xC0) >> 6) + 1
