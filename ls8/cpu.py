"""CPU functionality."""

import sys

# opcodes for branch table
ADD = 0b10100000
HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JNE = 0b01010110
JEQ = 0b01010101
JMP = 0b01010100

# reserve register for stack pointer
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.fl = 0
        self.branch_table = {
            ADD: self.add,
            HLT: self.halt,
            LDI: self.ldi,
            PRN: self.prn,
            MUL: self.multiply,
            POP: self.pop,
            PUSH: self.push,
            CALL: self.call,
            RET: self.ret,
            CMP: self.cmp,
            JNE: self.jne,
            JEQ: self.jeq,
            JMP: self.jmp
            }
    def add(self, op_a, op_b):
        self.reg[op_a] += self.reg[op_b]
        self.pc += 3

    def cmp(self, op_a, op_b):
        if self.reg[op_a] == self.reg[op_b]:
            self.fl = "E"
        elif self.reg[op_a] < self.reg[op_b]:
            self.fl = "LT"
        elif self.reg[op_a] > self.reg[op_b]:
            self.fl = "GT"
        self.pc += 3

    def jeq(self, op_a, op_b):
        if self.fl == "E":
            self.pc = self.reg[op_a]
        else:
            self.pc += 2
            
    def jmp(self, op_a, op_b):
        self.pc = self.reg[op_a]

    def jne(self, op_a, op_b):
        if self.fl != "E":
            self.pc = self.reg[op_a]
        else:
            self.pc += 2
    
    def call(self, op_a, op_b):
        self.reg[SP] -= 1
        self.ram_write(self.pc + 2, self.reg[SP])
        self.pc = self.reg[op_a]
    
    def ret(self, op_a, op_b):
        self.pc = self.ram[self.reg[SP]]
        self.reg[SP] += 1        

    def halt(self, op_a, op_b):
        sys.exit(0)

    def ldi(self, op_a, op_b):
        self.reg[op_a] = op_b
        self.pc += 3

    def prn(self, op_a, op_b):
        print(self.reg[op_a])
        self.pc += 2

    def multiply(self, op_a, op_b):
        self.reg[op_a] *= self.reg[op_b]
        self.pc += 3

    def push(self, op_a, op_b):
        self.reg[SP] -= 1
        self.ram_write(self.reg[op_a], self.reg[SP])
        self.pc += 2

    def pop(self, op_a, op_b):
        value = self.ram_read(self.reg[SP])
        self.reg[op_a] = value
        self.reg[SP] += 1
        self.pc += 2
    
    def ram_read(self, mar):
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr
    
    def load(self, program):
        """Load a program into memory."""
        instructions = []
        with open(program) as f:
            for line in f:
                line = line.strip().split("#")
                try:
                    num = int(line[0], 2)
                except ValueError:
                    continue
                instructions.append(num)
            
        address = 0

        for instruction in instructions:
            self.ram[address] = instruction
            address += 1


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
            self.trace()
            op_code = self.ram[self.pc]
            operand_a , operand_b  = self.ram[self.pc + 1], self.ram[self.pc + 2]
            if op_code in self.branch_table:
                self.branch_table[op_code](operand_a, operand_b)
