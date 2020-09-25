"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.running = False
        self.instr = {
            0b10000010: self.LDI,
            0b10100010: self.MUL,
            0b01000111: self.PRN,
            0b00000001: self.HLT
        }

    def ram_read(self, location):
        return self.ram[location]

    def ram_write(self, location, payload):
        self.ram[location] = payload

    def HLT(self):
        self.running = False
        self.pc += 1
        sys.exit()

    def LDI(self):
        reg_num = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.register[reg_num] = value
        self.pc += 3

    def PRN(self):
        reg_num = self.ram[self.pc + 1]
        print(self.register[reg_num])
        self.pc += 2


    def load(self):
        """Load a program into memory."""
        """
            open a file
            with open("fiolename") as f:
                for line in f:
                    print(line)
                    
            get from command line 
            sys.exit(1)
        """
        address = 0
        if len(sys.argv) != 2:
            print("no file given to run")
        try:
            with open(sys.argv[1], "r") as file:
                program = file.readlines()

                for instruction in program:
                    if instruction.startswith("#"):
                        continue
                    split_inst = instruction.split(' ')[0]
                    stripped_inst = split_inst.strip()
                    if stripped_inst == '':
                        continue
                    self.ram[address] = int(stripped_inst, 2)
                    address += 1
        except FileNotFoundError:
            print(f"could not find file {sys.argv[1]}")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]

        if op == "MUL":
            self.register[reg_a] *= self.register[reg_b]

        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")
        self.pc += 3

    def MUL(self, op1=None, op2=None):
        self.alu("MUL", op1, op2)

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
            instruction = self.ram_read(self.pc)
            if instruction in self.instr:
                if bin(instruction >> 5 & 0b001) == bin(0b1):
                    self.instr[instruction](op1=self.ram_read(self.pc + 1), op2 = self.ram_read(self.pc + 2))
                else:
                    self.instr[instruction]()

            # ir1 = self.ram_read(self.pc + 1)
            # ir2 = self.ram_read(self.pc + 2)
            # test = 0b11110000
            # binary = bin(test & 3)
            #
            # print(binary)
            # print(bin(instruction >> 5 & 0b001) == bin(0b1))
            # if instruction == 0b00000001: #  HLT
            #     self.HLT()
            # elif instruction == 0b10000010:  #  LDI
            #     self.LDI()
            # elif instruction == 0b01000111: #PRN
            #     self.PRN()
            # elif bin(instruction >> 5 & 0b001) == bin(0b1):
            #     if bin(instruction & 3) == bin(0b0):
            #         self.alu("ADD", ir1, ir2)
            #     elif bin(instruction & 3) == bin(0b10):
            #         self.alu('MUL', ir1, ir2)