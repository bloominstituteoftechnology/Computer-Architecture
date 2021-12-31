"""CPU functionality."""

import sys
from datetime import datetime

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
CALL = 0b01010000
RET = 0b00010001
PUSH = 0b01000101
POP = 0b01000110
ST = 0b10000100
PRA = 0b01001000
INT = 0b01010010
JMP = 0b01010100
IRET = 0b00010011


# ALU
MUL = 0b10100010  # 00000aaa 00000bbb
ADD = 0b10100000


class CPU:
    """Main CPU class."""

    def hdlr_LDI(self, operands): self.reg[operands[0]] = operands[1]
    def hdlr_PRN(self, operands): print(self.reg[operands[0]])

    def hdlr_CALL(self, operands):
        self.push(self.pc+1)
        self.pc = self.reg[operands[0]] - 2

    def hdlr_RET(self, operands): self.pc = self.pop()
    def hdlr_PUSH(self, operands): self.push(self.reg[operands[0]])
    def hdlr_POP(self, operands): self.reg[operands[0]] = self.pop()

    def hdlr_ST(
        self, operands): self.ram[self.reg[operands[0]]] = self.reg[operands[1]]

    def hdlr_PRA(self, operands):
        print(chr(self.reg[operands[0]]))

    def hdlr_JMP(self, operands): self.pc = self.reg[operands[0]]-2

    def hdlr_IRET(self, operands):
        for i in range(7):
            self.reg[6-i] = self.pop()
        self.fl = self.pop()
        self.pc = self.pop()-1

    def interupt(self):
        maskedInterrupts = self.reg[5] & self.reg[6]
        vector = 0xF8
        for i in range(8):
            if (maskedInterrupts >> i) & 1:
                self.hdlr_INT([vector + i])
                break

    def hdlr_INT(self, operands):
        self.reg[6] = 0
        self.push(self.pc)
        self.push(self.fl)
        for i, r in enumerate(self.reg):
            if i != 7:
                self.push(r)
        self.pc = self.ram[operands[0]]

    def push(self, data):
        self.ram[self.reg[7]] = data
        self.reg[7] -= 1

    def pop(self):
        self.reg[7] += 1
        data = self.ram[self.reg[7]]
        self.ram[self.reg[7]] = None
        return data

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0, 0, 0, 0, 0, 0, 0, 0xF3]
        self.pc = 0
        self.fl = 0
        self.running = False

        self.switcher = {
            LDI: self.hdlr_LDI,
            PRN: self.hdlr_PRN,
            CALL: self.hdlr_CALL,
            RET: self.hdlr_RET,
            PUSH: self.hdlr_PUSH,
            POP: self.hdlr_POP,
            ST: self.hdlr_ST,
            INT: self.hdlr_INT,
            PRA: self.hdlr_PRA,
            JMP: self.hdlr_JMP,
            IRET: self.hdlr_IRET
        }

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""
        fname = sys.argv[1]
        with open(fname, "r") as program:
            address = 0

            for instruction in program:
                if instruction[0] == '#' or instruction == "\n":
                    continue
                instruction = int(str.split(instruction, "#")
                                  [0].strip(), 2)
                self.ram[address] = instruction
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
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
        self.running = True
        prev_time = datetime.now()
        while self.running:
            time = datetime.now()
            if (time - prev_time).seconds >= 1:
                prev_time = time
                self.reg[6] = self.reg[6] | 0b1
            IR = self.ram[self.pc]
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]

            ALU = (IR >> 5) & 0b001
            if self.reg[6] != 0:
                self.interupt()
            elif IR == HLT:
                self.running = False
            elif ALU:
                self.alu(IR, operand_a, operand_b)
            else:
                self.switcher[IR]([operand_a, operand_b])
                self.pc += (IR >> 6) + 1

        pass
