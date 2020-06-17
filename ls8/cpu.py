"""CPU functionality."""

import sys
import re

# inst = {
#     "LDI": 0b10000010,  # Sets the Value of a reg to an int
#     "HLT": 0b00000001,  # halts the program, "ends it"/"stops it"
#     "PRN": 0b01000111,  # Prints the value at the next reg
#     "MUL": 0b10100010,  # multiply reg at +1 with reg at +2
# }


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0] * 8
        self.pc = 0
        self.is_run = False
        pass

    def ram_read(self, mar):
        print("MAR: ", mar)
        return self.reg[mar]

    def ram_write(self, mdr, value):

        self.reg[mdr] = value

        return print("RAM_WRITE: ", self.reg[mdr])

    def load(self, prog_file):
        """Load a program into memory."""

        prog = open(prog_file, "r")
        address = 0
        # program = []

        for inst in prog:
            # print("Inst: ", inst)
            if "1" in inst or "0" in inst:
                inst = inst[slice(8)]
                # inst = inst[0]
                self.ram[address] = int(inst, 2)
                address += 1

        print("RAM: ", self.ram)
        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = int(instruction)
        #     address += 1
        # print("RAM: ", self.ram)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def LDI(self):
        self.ram_write(
            self.ram[self.pc + 1], self.ram[self.pc + 2])
        # print(self.ram[])
        # print("PC + 1: ", self.ram[self.pc + 1])
        # print("PC + 2: ", self.ram[self.pc + 2])
        self.pc += 3
        # run = False

    def HLT(self):
        self.is_run = False
        self.pc += 1

    def PRN(self):
        index = int(str(self.ram[self.pc + 1]), 2)
        value = self.reg[index]
        print(f"Value: {value}, Register Index : {index}")
        self.pc += 2

    def MUL(self):
        num1 = self.ram_read(self.ram[self.pc + 1])
        num2 = self.ram_read(self.ram[self.pc + 2])
        print("MUL answere: ", num1 * num2)
        self.pc += 3

    def call_stack(self, n):
        stack = {
            0b10000010: self.LDI,
            0b00000001: self.HLT,
            0b01000111: self.PRN,
            0b10100010: self.MUL,

        }
        if n in stack:
            stack[n]()
        else:
            print(f"No instrunction found! IR: {bin(int(n,2))}")
            sys.exit(1)

    def run(self):
        """Run the CPU."""
        self.is_run = True

        while self.is_run:
            ir = self.ram[self.pc]  # the instruction or code to run
            self.call_stack(ir)

            # if ir == inst["LDI"]:
            #     self.ram_write(
            #         self.ram[self.pc + 1], self.ram[self.pc + 2])
            #     # print(self.ram[])
            #     # print("PC + 1: ", self.ram[self.pc + 1])
            #     # print("PC + 2: ", self.ram[self.pc + 2])
            #     self.pc += 3
            #     # run = False

            # elif ir == inst["HLT"]:
            #     run = False
            #     self.pc += 1

            # elif ir == inst["PRN"]:
            #     index = int(str(self.ram[self.pc + 1]), 2)
            #     value = self.reg[index]
            #     print(f"Value: {value}, Register Index : {index}")
            #     self.pc += 2

            # elif ir == inst["MUL"]:
            #     num1 = self.ram_read(self.ram[self.pc + 1])
            #     num2 = self.ram_read(self.ram[self.pc + 2])
            #     print("MUL answere: ", num1 * num2)
            #     self.pc += 3

            # else:
            #     print(f"No instrunction found! IR: {bin(int(ir,2))}")
            #     sys.exit(1)
