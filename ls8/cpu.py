"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        # R07 STACK POINTER
        self.reg[7] = 0xF4
        self.pc = 0
        self.isRunning = True

        # self.instruction_translate = {
        #     0b00000001: "HLT",
        #     0b10000010: "LDI",
        #     0b01000111: "PRN",
        #     0b10100010: "MUL"
        # }
        # self.instruction_set = {
        #     "HLT": self.HLT,
        #     "LDI": self.LDI,
        #     "PRN": self.PRN,
        #     "MUL": self.MUL
        # }
        self.instruction_set = {
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MUL,
            0b01000110: self.POP,
            0b01000101: self.PUSH,
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b10100000: self.ADD

        }

    def ram_write(self, val, addy):
        self.ram[addy] = val

    def ram_read(self, addy):
        return self.ram[addy]


    def load(self, program):
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

        for instruction in program:
            # print("{0:b}".format(instruction))
            # print(instruction)
            # print()
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] = 255 & (self.reg[reg_a] + self.reg[reg_b])
        elif op == "MUL":
            self.reg[reg_a] = 255 & (self.reg[reg_a] * self.reg[reg_b])
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


        while self.isRunning:

            # Grab the bytecode instruction out of memory
            # Use the instruction to access or branch table
            if self.ram_read(self.pc) not in self.instruction_set:
                print("We found something out of the ordinary!")
                print("{0:b}".format(self.ram_read(self.pc)))
                print(self.ram_read(self.pc))
                return 1
            self.instruction_set[self.ram_read(self.pc)]()

    def LDI(self):
        reg_a = self.ram_read(self.pc + 1)
        int = self.ram_read(self.pc + 2)
        self.reg[reg_a] = 255 & int
        self.pc += 3

    def ADD(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3

    def MUL(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3

    def PRN(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc += 2

    def HLT(self):
        self.isRunning = False

    def POP(self):
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.reg[7])
        self.reg[7] += 1
        self.pc += 2

    def PUSH(self):
        self.reg[7] -= 1
        self.ram[self.reg[7]] = self.reg[self.ram_read(self.pc + 1)]
        self.pc += 2

    def CALL(self):
        # Subroutine Address
        # - Instruction after PC contains register
        # - Use that to access the value inside the register
        # - Store it into a variable sub_add
        sub_add = self.reg[self.ram_read(self.pc + 1)]

        # Start at current instruction + 2
        # keep moving forward until we find an instruction
        # This is where we want to continue after we come back
        ret_add = self.pc + 2
        while self.ram_read(ret_add) not in self.instruction_set:
            ret_add += 1

        # PUSH the address we want to return to onto the stack
        # So that we may access it from anywhere else
        self.reg[7] -= 1
        self.ram[self.reg[7]] = ret_add
        # Set the PC to the address we extracted earlier
        self.pc = sub_add

    def RET(self):
        # Store value at the current top of the stack into PC
        self.pc = self.ram_read(self.reg[7])
        self.reg[7] += 1
