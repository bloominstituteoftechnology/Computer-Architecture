"""CPU functionality."""

import sys
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP =  0b01000110
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        # is computer running:
        self.running = False
        # 256-byte RAM, each element is 1 byte (can only store integers 0-255)
        self.ram = [0] * 256

        # R0-R7: 8-bit general purpose registers, R5 = interrupt mask (IM), 
        # R6 = interrupt status (IS), R7 = stack pointer (SP)
        self.reg = [0] * 8

        # Internal Registers
        self.pc = 0 # Program Counter: address of the currently executing instruction
        # Instruction Register: contains a copy of the currently executing instruction
        self.mem_add = 0 # Memory Address Register: holds the memory address we're reading or writing
        # Memory Data Register: holds the value to write or the value just read
        self.fl = 0 # Flag Register: holds the current flags status
        self.SP = 7

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == 'MULT':
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
        self.running = True
        while self.running:
            ir = self.ram_read(self.pc)  # Instruction register
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == HLT: 
                self.running = False
            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif ir == PUSH:
                SP -= 1
                self.ram_write(SP, self.reg[operand_a])
                self.pc += 2
            elif ir == POP:
                self.trace()
                self.reg[operand_a] = self.ram[SP]
                SP += 1
                self.pc +=2

    def ram_read(self, mem_add):
        return self.ram[mem_add]

    def ram_write(self, mem_add, value):
        self.ram[mem_add] = value