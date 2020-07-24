"""CPU functionality."""

import sys

HTL = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000

CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.branch_table = {}
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.reg[7] = 0xF4   # Stack Pointer
        self.pc = 0          # Program Counter, address of the currently executing instruction

        # Flags
        self.E = None
        self.L = None
        self.G = None

        # Instructions
        self.branch_table[HTL] = self.hlt_inst
        self.branch_table[LDI] = self.ldi_inst
        self.branch_table[PRN] = self.prn_inst
        self.branch_table[MUL] = self.mul_inst
        self.branch_table[PUSH] = self.push_inst
        self.branch_table[POP] = self.pop_inst
        self.branch_table[ADD] = self.add_inst
        self.branch_table[RET] = self.ret_inst
        self.branch_table[CALL] = self.call_inst

        # Instructions - Sprint Challenge
        self.branch_table[CMP] = self.cmp_inst
        self.branch_table[JMP] = self.jmp_inst
        self.branch_table[JEQ] = self.jeq_inst
        self.branch_table[JNE] = self.jne_inst

        # IR    // Instruction Register, contains a copy of the currently executing instruction
        # MAR   // Memory Address Register, holds the memory address we're reading or writing
        # MDR   // Memory Data Register, holds the value to write or the value just read
        # R5    // Reserved as the interrupt mask (IM)
        # R6    // Reserved as the interrupt status (IS)
        # R7    // Reserved as the stack pointer (SP)

    def ram_read(self, MAR):
        if MAR < len(self.ram):
            return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        if MAR < len(self.ram):
            self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""
        while True:
            IR = self.ram_read(self.pc)
            # print(IR,"\n")
            if IR in self.branch_table:
                self.branch_table[IR]()
            else:
                print("ERROR:", IR)

    def hlt_inst(self):
        exit(1)

    def mul_inst(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)

        result = self.reg[reg_a] * self.reg[reg_b]
        self.reg[reg_a] = result
        self.pc += 3

    def add_inst(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)

        result = self.reg[reg_a] + self.reg[reg_b]
        self.reg[reg_a] = result
        self.pc += 3

    def ldi_inst(self):
        MAR = self.ram_read(self.pc + 1)
        MDR = self.ram_read(self.pc + 2)

        if MAR < len(self.ram):
            self.reg[MAR] = MDR
        self.pc += 3

    def prn_inst(self):
        operand_a = self.ram_read(self.pc + 1)

        print(self.reg[operand_a])
        self.pc += 2

    def push_inst(self):
        self.reg[7] -= 1
        operand_a = self.ram_read(self.pc + 1)
        self.ram[self.reg[7]] = self.reg[operand_a]
        self.pc += 2

    def pop_inst(self):
        operand_a = self.ram_read(self.pc + 1)
        self.reg[operand_a] = self.ram_read(self.reg[7])
        self.reg[7] += 1
        self.pc += 2

    def ret_inst(self):
        self.pc = self.ram_read(self.reg[7])
        self.reg[7] += 1

    def call_inst(self):
        temp = self.ram_read(self.pc + 1)
        sub = self.reg[temp]

        ret = self.pc + 2
        while self.ram_read(ret) not in self.branch_table:
            ret += 1

        self.reg[7] -= 1
        self.ram[self.reg[7]] = ret
        self.pc = sub

    def jmp_inst(self):
        # print("JMP")
        reg_a = self.ram_read(self.pc + 1)
        self.pc = self.reg[reg_a]

    def jeq_inst(self):
        # print("JEQ")
        if self.E == 1:
            self.jmp_inst()
        else:
            self.pc += 2

    def jne_inst(self):
        # print("JNE")
        if self.E == 0:
            self.jmp_inst()
        else:
            self.pc += 2

    def cmp_inst(self):
        # print("CMP")
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)

        if self.reg[reg_a] == self.reg[reg_b]:
            self.E = 1
        else:
            self.E = 0

        if self.reg[reg_a] < self.reg[reg_b]:
            self.L = 1
        else:
            self.L = 0

        if self.reg[reg_a] > self.reg[reg_b]:
            self.G = 1
        else:
            self.G = 0

        self.pc += 3


    def load(self, file):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("usage: comp.py filename")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    try:
                        line = line.split("#", 1)[0]
                        line = int(line, 2)
                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass

        except FileNotFoundError:
            print(f"Couldn't find file {sys.argv[1]}")
            sys.exit(1)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        #
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        # print(self.ram)

    def alu(self, op):
        """ALU operations."""

        if op == "AND":
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
            self.pc += 3
        elif op == "OR":
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
            self.pc += 3
        elif op == "XOR":
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
            self.pc += 3
        elif op == "NOT":
            reg_a = self.ram_read(self.pc + 1)
            self.reg[reg_a] = ~self.reg[reg_a]
            self.pc += 2
        elif op == "SHR":
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
            self.pc += 3
        elif op == "SHL":
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
            self.pc += 3
        elif op == "MOD":
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            if self.reg[reg_b] == 0:
                self.hlt_inst()
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
            self.pc += 3
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
