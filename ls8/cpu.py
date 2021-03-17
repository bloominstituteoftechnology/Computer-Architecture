"""CPU functionality."""

import sys

# opcodes
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
CALL = 0b01010000
CMP = 0b10100111
MUL = 0b10100010

sys_file = ""
if len(sys.argv) < 2:
    print("In terminal must provide: python3 ls8.py <path-to-program-file>")
else:
    sys_file = sys.argv[1]


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 255
        self.register = [0] * 8

    def load(self):
        """Load a program into memory."""
        new_program = []
        if sys_file:
            with open(sys_file) as new_file:
                for line in new_file:
                    new_code = line.split('#')[0].strip()
                    # take out blank lines
                    if new_code == "":
                        continue
                    # change str to int
                    new_code_i = int(new_code, 2)
                    new_program.append(new_code_i)
                print("new_program", new_program)
        else:
            quit()
            print(FileNotFoundError)

        address = 0

        for instruction in new_program:
            self.ram[address] = instruction
            address += 1

        # # For now, we've just hardcoded a program:
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
        #     self.ram[address] = instruction
        #     address += 1

    def ram_read(self, ram_address):
        return self.ram[ram_address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def CALL(self):
        # I believe this is like a repeat: change self.pc = to the value in the next self.ram
        ram_index = self.ram[self.pc + 1]
        self.pc = ram_index

    def CMP(self):
        index_a = self.ram[self.pc + 1]
        index_b = self.ram[self.pc + 2]
        value_a = self.register[index_a]
        value_b = self.register[index_b]
        if value_a < value_b:
            self.ram[index_a] = self.ram[index_a] & 11111100
        elif value_a > value_b:
            self.ram[index_a] = self.ram[index_a] & 11111010
        else:
            self.ram[index_a] = self.ram[index_a] & 11111001
        self.pc += 3

    def HLT(self):
        running = False

    def LDI(self):
        num = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.register[num] = value
        self.pc += 3

    def MUL(self):
        reg_index_a = self.ram[self.pc + 1]
        reg_index_b = self.ram[self.pc + 2]
        self.register[reg_index_a] = self.register[reg_index_a] * \
            self.register[reg_index_b]
        self.pc += 3

    def PRN(self):
        reg_index = self.ram[self.pc + 1]
        print(self.register[reg_index])
        self.pc += 2

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

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            # fetch
            inst = self.ram[self.pc]

            # decode
            if inst == LDI:
                self.LDI()

            elif inst == MUL:
                self.MUL()

            elif inst == PRN:
                self.PRN()

            elif inst == HLT:
                self.HLT()

            else:
                print("Command not understood")
