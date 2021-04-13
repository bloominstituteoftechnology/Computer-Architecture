"""CPU functionality."""
#
import sys

#instruction set:
HLT = 0
LDI = 0, 8
PRN = 0

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.registers = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
#not really sure where to put this
        running = True

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

    def ram_read(self, address):
        for value in address:
            self.ram[address.value] = value
            return value

    def ram_write(newvalue, address):
        for value in address:
            value.replace(value, newvalue)
            return value

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

#From the spec:
#When the LS-8 is booted, the following steps occur:

#R0-R6 are cleared to 0.
#R7 is set to 0xF4.
#PC and FL registers are cleared to 0.
#RAM is cleared to 0.
#Subsequently, the program can be loaded into RAM starting at address 0x00.

    def run(self, pc):
        instruction = self.ram[pc]
        operand_a = self.ram[pc + 1]
        operand_b = self.ram[pc + 2]
#potential structure for LDI
        if instruction == LDI:
            reg_index = operand_a
            num = operand_b
            num = int(self.registers[reg_index])
            print(num)
            pc += 3
#potential structure for PRN
        elif instruction == PRN:
            reg_index = operand_a
            num = self.registers[reg_index]
            print(num)
            pc += 2
#potential structure for HLT
        elif instruction == HLT:
            running = False
            sys.exit(0)

        else:
            print("WRONG WAY")
            sys.exit(1)