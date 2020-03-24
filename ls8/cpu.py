"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        pass

    def load(self, filename):
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
        try:
            with open(filename) as f:
                for line in f:
                    comment_split = line.split('#')
                    num = comment_split[0].strip()
                    if num == '':
                        continue
                    instruction = int(num, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print('file not found')
            sys.exit(2)

        


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")
    def ram_read(self, index):
        print(self.ram[index])
    def ram_write(self, index, value):
        self.ram[index] = value

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
        halt = False
        while halt is False:
            instruction = self.ram[self.pc]
            if instruction == 0b10000010:
                register = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[register] = value
                self.pc += 3
                print('tis working')
            elif instruction == 0b01000111:
                register = self.ram[self.pc + 1]
                print(self.reg[register])
                self.pc += 2
            elif instruction == 0b00000001:
                halt = True
            elif instruction == 0b10100010:
                value_1 = self.ram[self.pc + 1]
                value_2 = self.ram[self.pc + 2]
                self.alu('MUL', value_1, value_2)
                self.pc += 3
            else:
                print('instruction not found')
                halt = True
     


