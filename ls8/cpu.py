"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        # General Purpose Registers
        self.registers = [0] * 8

        # Internal Registers
        self.pc = 0
        self.ir = 0
        # self.mar = 0
        # self.mdr = 0
        self.fl = 0

        # Instructions
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001

        # RAM
        self.ram = [0] * 256

    def load(self):
        """Load a program into memory."""

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
        # ]

        program = []

        with open(sys.argv[1]) as f:
            program = [line.strip('\n') for line in f]

        program = [int(i[:8], 2) for i in program if len(i) > 1 if i[0] != '#']

        # print(program)

        for instruction in program:
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

    def ram_read(self, read_value):
        return self.registers[read_value]

    def ram_write(self, write_value, write_address_location):
        self.registers[write_address_location] = write_value

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            instruction = self.ram[self.pc]

            if instruction == self.LDI:
                MAR = self.ram[self.pc + 1]
                MDR = self.ram[self.pc + 2]

                self.ram_write(MDR, MAR)

                self.pc += 2

            elif instruction == self.PRN:
                MAR = self.ram[self.pc + 1]
                print(self.ram_read(MAR))

                self.pc += 1

            elif instruction == self.HLT:
                print("Exiting program.")
                running = False

            else:
                print("Unknown Instruction. Exiting Program.")
                running = False

            self.pc += 1
