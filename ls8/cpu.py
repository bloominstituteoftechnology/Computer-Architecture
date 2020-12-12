"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.registers = [0] * 8
        self.registers[7] = 0xF4
        self.pc = 0
        self.ram = [0] * 256
        self.halted = False
        self.fl = 0

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        # open the file
        with open(filename) as my_file:
            # go through each line to parse and get instruction
            for line in my_file:
                # try and get the instruction/operand in the line
                comment_split = line.split("#")
                maybe_binary_number = comment_split[0]
                try:
                    x = int(maybe_binary_number, 2)
                    self.ram_write(x, address)
                    address += 1
                except:
                    continue

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == MUL:
            self.registers[reg_a] *= self.registers[reg_b]
            self.pd += 3
        else:
            raise Exception("Unsupported ALU operation")
        if op == CMP:
            if self.registers[reg_a] == self.registers[reg_b]:
                self.fl = 1
            if self.registers[reg_a] < registers[reg_b]:
                self.fl = 1
            if self.registers[reg_a] > registers[reg_b]:
                self.fl = 1
            else:
                self.fl = 0

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""

        while not self.halted:
            instruction_to_execute = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.execute_instruction(instruction_to_execute, operand_a, operand_b)

    def execute_instruction(self, instruction, operand_a, operand_b):
        if instruction == HLT:
            self.halted = True
            self.pc += 1
        elif instruction == PRN:    
            print(self.registers[operand_a])
            self.pc += 2
        elif instruction == LDI:
            self.registers[operand_a] = operand_b
            self.pc += 3
        elif instruction == MUL:
            self.alu(instruction, operand_a, operand_b)
        elif instruction == PUSH:
            # decrement the stack pointer
            self.registers[SP] -= 1
            # store the operand ine the stack
            self.ram_write(self.registers[operand_a], self.registers[SP])
            self.pc += 2
        elif instruction == POP:
            self.registers[operand_a] = self.ram_read(self.registers[SP])
            self.pc += 2
        elif instruction == CALL:
            # self.registers[SP] -= 1
            # address_of_next_instruction = self.pc + 2
            pass
        elif instruction == RET:
            pass


        elif instruction == CMP:
            self.alu(instruction, operand_a, operand_b)
        elif instruction == JMP:
            self.pc = self.registers[operand_a]
        elif instruction == JEQ:
            if self.fl = 1:
                self.pc = self.registers[operand_a]
        elif instruction == JNE:
            if self.fl = 0:
                self.pc = self.registers[operand_a]


        else:
            print('idk what to do.')
            pass
