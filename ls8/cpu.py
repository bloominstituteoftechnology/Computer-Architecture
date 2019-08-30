"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.hlt = False

        self.ops = {
            LDI: self.op_ldi,
            PRN: self.op_prn,
            HLT: self.op_hlt,
            MUL: self.op_mul
        }
    # op functions
    def op_ldi(self, address, value):
        self.reg[address] = value

    def op_prn(self, address, op_b): #op a/b
        print(self.reg[address]) #op_a acts as address

    def op_hlt(self, op_a, op_b):
        self.hlt = True
    
    def op_mul(self, operand_a, operand_b):
        self.alu('MUL', operand_a, operand_b)

    # ram functions 

    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self[address] = value

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        with open(filename) as file:
            for line in file:
                comment_split = line.split('#') # used to ignore comments
                instruction = comment_split[0]
                if instruction == '':
                    continue
                elif (instruction[0] == '0') or (instruction[0] == '1'):
                    self.ram[address] = int(instruction[:8], 2)
                    address += 1

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

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
        while self.hlt == False:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            op_size = ir >> 6
            ins_set = ((ir >> 4) & 0b1) == 1
            if ir in self.ops:
                self.ops[ir](operand_a, operand_b)
            if not ins_set:
                self.pc += op_size + 1