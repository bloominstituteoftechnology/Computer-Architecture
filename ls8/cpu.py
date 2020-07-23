"""CPU functionality."""

import sys


LDI = 0b10000010 
PRN = 0b01000111 # Print
HLT = 0b00000001  # Halt
MUL = 0b10100010  # Multiply
ADD = 0b10100000  # Addition
SUB = 0b10100001 # Subtraction
DIV = 0b10100011 # Division
PUSH = 0b01000101 # Stack Push
POP = 0b01000110 # Stack Pop
SP = 7 # Stack pointer

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.reg[7] = 0xF4


    def load(self):
        """Load a program into memory."""
        filename = sys.argv[1]

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        #    ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        with open(filename) as f:
            for line in f:
                line = line.split("#")[0].strip()
                if line == "":
                    continue
                else:
                    self.ram[address] = int(line, 2)
                    address += 1



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
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

    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, address, value):
        self.ram[address] = value
    
    def HLT(self):
        self.running = False

    def run(self):
        """Run the CPU."""
        self.load()
        while self.running:
            instruction_register = self.ram[self.pc]
            reg_a = self.ram[self.pc + 1]
            reg_b = self.ram[self.pc + 2]

            if instruction_register == HLT:
                self.running = False
                self.pc += 1
            elif instruction_register == LDI:
                self.reg[reg_a] = reg_b
                self.pc += 3
            elif instruction_register == PRN:
                print(self.reg[reg_a])
                self.pc += 2
            elif instruction_register == MUL:
                self.reg[reg_a] *= self.reg[reg_b]
                self.pc += 3
            elif instruction_register == PUSH:
                self.reg[SP] -= 1
                stack_address = self.reg[SP]
                register_number = self.ram_read(self.pc + 1)
                register_number_value = self.reg[register_number]
                self.ram_write(stack_address, register_number_value)
                self.pc += 2
            elif instruction_register == POP:
                stack_value = self.ram_read(self.reg[SP])
                register_number = self.ram_read(self.pc + 1)
                self.reg[register_number] = stack_value
                self.reg[SP] += 1 
                self.pc += 2
            else:
                print(f"Instruction '{instruction_register}'' at address '{self.pc}' is not recognized")
                self.pc += 1

