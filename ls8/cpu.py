"""CPU functionality."""

from ls8Instructions import *
import sys
import time

IM = 5
IS = 6
SP = 7
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
        self.lastFire = time.time()
        self.interruptsEnabled = True

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
        self.branchtable[ST] = self.handleST
        self.branchtable[JMP] = self.handleJMP
        self.branchtable[PRA] = self.handlePRA
        self.branchtable[IRET] = self.handleIRET

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
        """
        mar is the address
        mdr is the data to store at that address
        """
        self.ram[mar] = mdr

    def alu(self, op, operandA, operandB):
        """ALU operations."""

        if op == MUL:
            self.register[operandA] *= self.register[operandB]
            self.register[operandA] &= 0xFF
        elif op == ADD:
            self.register[operandA] += self.register[operandB]
            self.register[operandA] &= 0xFF
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
    
    def handleST(self):
        operandA = self.ramRead(self.pc + 1)
        operandB = self.ramRead(self.pc + 2)
        self.ramWrite(self.register[operandB], self.register[operandA])

    def handleJMP(self):
        operand = self.ramRead(self.pc + 1)
        self.pc = self.register[operand]

    def handlePRA(self):
        operand = self.ramRead(self.pc + 1)
        value = self.register[operand]
        print(chr(value))

    def handleIRET(self):
        self.register[6] = self.popValueFromStack()
        self.register[5] = self.popValueFromStack()
        self.register[4] = self.popValueFromStack()
        self.register[3] = self.popValueFromStack()
        self.register[2] = self.popValueFromStack()
        self.register[1] = self.popValueFromStack()
        self.register[0] = self.popValueFromStack()
        self.fl = self.popValueFromStack()
        self.pc = self.popValueFromStack()
        self.interruptsEnabled = True

    def __interuptTimer(self):
        currentTime = time.time()
        if currentTime > self.lastFire + 1:
            self.lastFire = currentTime
            self.register[6] = self.register[6] | 0b1

    def run(self):
        """Run the CPU."""

        while True:
            self.__interuptTimer()

            # check for interrupts
            if self.interruptsEnabled:
                maskedInterrupts = self.register[IM] & self.register[IS]
                for i in range(8):
                    interrupt = ((maskedInterrupts >> i) & 1) == 1
                    if interrupt:
                        self.interruptsEnabled = False
                        # clear only the bit of the current interrupt
                        self.register[IS] &= 0xFF ^ (1 << i)
                        self.pushValueOnStack(self.pc)
                        self.pushValueOnStack(self.fl)
                        self.pushValueOnStack(self.register[0])
                        self.pushValueOnStack(self.register[1])
                        self.pushValueOnStack(self.register[2])
                        self.pushValueOnStack(self.register[3])
                        self.pushValueOnStack(self.register[4])
                        self.pushValueOnStack(self.register[5])
                        self.pushValueOnStack(self.register[6])
                        newAddress = self.ramRead(0xF8 + i)
                        self.pc = newAddress
                        break

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
