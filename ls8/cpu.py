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
        self.setupBranchtable()

    def setupBranchtable(self):
        self.branchtable = {}

        self.branchtable[LDI] = self.handleLDI
        self.branchtable[PRN] = self.handlePRN
        self.branchtable[HLT] = self.handleHLT
        self.branchtable[MUL] = self.handleMUL
        self.branchtable[PUSH] = self.handlePUSH
        self.branchtable[POP] = self.handlePOP
        self.branchtable[CALL] = self.handleCALL
        self.branchtable[RET] = self.handleRET
        self.branchtable[ADD] = self.handleADD

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
        elif op == ADD:
            self.register[operandA] += self.register[operandB]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE (pc): %02X | (values at pc, pc+1, pc+2) %02X %02X %02X | REGISTERS: " % (
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

    def handleLDI(self):
        operandIndex = self.ramRead(self.pc + 1)
        operand = self.ramRead(self.pc + 2)
        self.register[operandIndex] = operand

    def handlePRN(self):
        operandIndex = self.ramRead(self.pc + 1)
        operand = self.register[operandIndex]
        print(operand)

    def handleHLT(self):
        sys.exit(0)

    def handleMUL(self):
        operandAIndex = self.ram[self.pc + 1]
        operandBIndex = self.ram[self.pc + 2]
        self.alu(MUL, operandAIndex, operandBIndex)
    
    def handleADD(self):
        operandAIndex = self.ram[self.pc + 1]
        operandBIndex = self.ram[self.pc + 2]
        self.alu(ADD, operandAIndex, operandBIndex)

    def handlePUSH(self):
        operandIndex = self.ramRead(self.pc + 1)
        operand = self.register[operandIndex]
        self.pushValueOnStack(operand)

    def pushValueOnStack(self, operand):
        stackPointer = self.getStackIndex() - 1
        self.setStackIndex(stackPointer)
        self.ramWrite(operand, stackPointer)

    def handlePOP(self):
        operand = self.popValueFromStack()
        operandIndex = self.ramRead(self.pc + 1)
        self.register[operandIndex] = operand

    def popValueFromStack(self):
        stackPointer = self.getStackIndex()
        self.setStackIndex(stackPointer + 1)
        return self.ramRead(stackPointer)

    def handleCALL(self):
        operandIndex = self.ramRead(self.pc + 1)
        operand = self.register[operandIndex]
        # save address of next *INSTRUCTION* in stack
        self.pushValueOnStack(self.pc + 2)
        self.pc = operand

    def handleRET(self):
        operand = self.popValueFromStack()
        self.pc = operand

    def run(self):
        """Run the CPU."""

        while True:
            instructionRegister = self.ram[self.pc]

            instructionMethod = self.branchtable.get(instructionRegister, None)

            # self.trace()
            if instructionMethod is not None:
                instructionMethod()
            else:
                print(f"Instruction not recognized: {instructionRegister}")
                exit(1)

            # check to see if the PC is explicitly set by the instruction. if not, increment the PC by the number of arguments + 1
            if ((instructionRegister >> 4) & 0b1) != 1:
                self.pc += ((instructionRegister & 0xC0) >> 6) + 1
            # print(f"about to execute {self.pc}")

