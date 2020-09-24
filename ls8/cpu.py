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
            instruction = self.ram_read(self.pc)
            if instruction == 0b00000001: #  HLT
                self.HLT()
            elif instruction == 0b10000010:  #  LDI
                self.LDI()
            elif instruction == 0b01000111: #PRN
                self.PRN()
