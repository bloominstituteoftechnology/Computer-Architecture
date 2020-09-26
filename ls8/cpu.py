"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.sp = 7  # pointer location in register
        self.reg[self.sp] = 0xF3  # Slot in memory 243
        self.fl = 0b00000000 # Flags Register
        self.running = False
        self.instr = {
            0b10000010: self.LDI,
            0b10100010: self.MUL,
            0b01000111: self.PRN,
            0b00000001: self.HLT,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b10100000: self.ADD,
            0b10100111: self.CMP,
            0b01010101: self.JEQ,
            0b01010110: self.JNE,
            0b01010100: self.JMP
        }

    def JMP(self, op1=None, op2=None):
        self.pc = self.reg[op1]

    def JNE(self, op1=None, op2=None):
        if (self.fl & 0b00000001) == 0:
            self.pc = self.reg[op1]
        else:
            self.pc += 2

    def JEQ(self, op1=None, op2=None):
        if self.fl & 0b00000001 == 1:
            self.pc = self.reg[op1]
        else:
            self.pc += 2


    def CALL(self, op1=None, op2=None):
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], self.pc + 2)
        self.pc =self.reg[op1]


    def RET(self, op1=None, op2=None):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1


    def PUSH(self, op1=None, op2=None):
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], self.reg[op1])
        self.pc += 2

    def POP(self, op1=None, op2=None):
        self.reg[op1] = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
        self.pc += 2

    def ram_read(self, op1=None):
        return self.ram[op1]

    def ram_write(self, op1=None, op2=None):
        self.ram[op1] = op2

    def HLT(self, op1=None, op2=None):
        self.running = False
        self.pc += 1
        sys.exit()

    def LDI(self, op1=None, op2=None):
        reg_num = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.reg[reg_num] = value
        self.pc += 3

    def PRN(self, op1=None, op2=None):
        print(self.reg[op1])
        self.pc += 2


    def load(self):
        """Load a program into memory."""

        address = 0
        if len(sys.argv) != 2:
            print("no file given to run")
        try:
            with open(sys.argv[1], "r") as file:
                program = file.readlines()

                for instruction in program:
                    if instruction.startswith("#"):
                        continue
                    split_inst = instruction.split(' ')[0]
                    stripped_inst = split_inst.strip()
                    if stripped_inst == '':
                        continue
                    self.ram[address] = int(stripped_inst, 2)
                    address += 1
        except FileNotFoundError:
            print(f"could not find file {sys.argv[1]}")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100

        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")
        self.pc += 3

    def MUL(self, op1=None, op2=None):
        self.alu("MUL", op1, op2)

    def ADD(self, op1=None, op2=None):
        self.alu("ADD", op1, op2)

    def CMP(self, op1=None, op2=None):
        self.alu("CMP", op1, op2)

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
        self.running = True
        while self.running:
            instruction = self.ram_read(self.pc)
            if instruction in self.instr:
                self.instr[instruction](self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
            else:
                print("Unknown Instruction Command")
                self.HLT()