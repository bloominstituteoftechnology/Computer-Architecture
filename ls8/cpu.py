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
        self.registers = [0] * 8 # R0-R7
        self.pc = 0 # Program Counter, address of the currently-executing instuction

        # "Variables" in hardware. Known as "registers".
        # There are a fixed number of registers
        # They have fixed names
        #  R0, R1, R2, ... , R6, R7

    # accepts the address to read and return the value stored there.
    def ram_read(self, address):
        return self.ram[address]

    # accepts a value to write, and the address to write it to
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        try:
            address = 0
            with open(sys.argv[1]) as file:
                for line in file:
                    split_file = line.split("#")
                    value = split_file[0].strip()
                    if value == "":
                        continue

                    try:
                        instruction = int(value, 2)
                    except ValueError:
                        print(f"Invalid number '{value}'")
                        sys.exit(1)

                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]} {sys.argv[1]} file not found")
            sys.exit()

        # address = 0
        #
        # # For now, we've just hardcoded a program:
        #
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
        self.running = True
        while self.running:
            instruction = self.ram_read(self.pc)  # Instruction register, copy of the currently-executing instruction

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction == HLT: # HLT - halt the CPU and exit the emulator.
                self.running = False
                self.pc += 1
            elif instruction == PRN:
                print(self.registers[operand_a])
                self.pc += 2
            elif instruction == LDI:
                self.registers[operand_a] = operand_b
                self.pc += 3
            elif instruction == MUL:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.registers[reg_a] = self.registers[reg_a] * self.registers[reg_b]
                self.pc +=3


# Glossary:
# immediate: takes a constant integer value as an argument
# register: takes a register number as an argument
# iiiiiiii: 8-bit immediate value
# 00000rrr: Register number
# 00000aaa: Register number
# 00000bbb: Register number
# Machine code values shown in both binary and hexadecimal.

# PRN
# PRN register pseudo-instruction
# Print numeric value stored in the given register.
# Print to the console the decimal integer value that is stored in the given register.
# Machine code:
# 01000111 00000rrr

# LDI
# LDI register immediate
# load "immediate", store a value in a register, or "set this register to this value".
# Set the value of a register to an integer.
# Machine code:
# 10000010 00000rrr iiiiiiii
