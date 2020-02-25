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

    def getStackIndex(self):
        return self.register[7]

    def setStackIndex(self, index):
        self.register[7] = index

    def ramRead(self, mar):
        return self.ram[mar]

    def ramWrite(self, mdr, mar):
        self.ram[mar] = mdr

    def alu(self, op, operandA, operandB):
        """ALU operations."""

        if op == MUL:
            self.register[operandA] *= self.register[operandB]
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
            self.ramRead(self.pc),
            self.ramRead(self.pc + 1),
            self.ramRead(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

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
                operandAIndex = self.ram[self.pc + 1]
                operandBIndex = self.ram[self.pc + 2]
                self.alu(instructionRegister, operandAIndex, operandBIndex)
            elif instructionRegister == PUSH:
                stackPointer = self.getStackIndex() - 1
                self.setStackIndex(stackPointer)
                regIndex = self.ramRead(self.pc + 1)
                value = self.register[regIndex]
                self.ramWrite(value, stackPointer)
            elif instructionRegister == POP:
                stackPointer = self.getStackIndex()
                value = self.ramRead(stackPointer)
                regIndex = self.ramRead(self.pc + 1)
                self.register[regIndex] = value
                self.setStackIndex(stackPointer + 1)
            elif instructionRegister == HLT:
                exit(0)
            else:
                print(f"Instruction not recognized: {instructionRegister}")
                exit(1)

            # offset pc by whatever the previous register said to offset by (MIGHT be problematic here, but for now is DRY)
            self.pc += ((instructionRegister & 0xC0) >> 6) + 1
