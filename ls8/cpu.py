"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.PC = 0
        self.IR = 0
        self.MAR = 0
        self.MDR = 0
        self.FL = 0b00000000
        self.IM = self.reg[5]
        self.IS = self.reg[6]
        self.SP = self.reg[7]
        self.ram = [0] * 256

    def load(self):
        """Load a program into memory."""
        address = 0
        if len(sys.argv) != 2:
            print('Wrong amount of args. \nUsage example: python ls8.py aprogram.ls8')
            sys.exit(1)

        program_file = open(sys.argv[1])

        for line in program_file:

            inst = line.strip()
            if not inst.startswith('#'):
                inst = inst.split('#', 1)[0]

                inst = inst.split()[0]

                inst = int(inst, 2)
                self.ram[address] = inst
                address += 1

    # sprint challenge material
    # Adding flag and CMP instruction to the alu
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            x, y = self.reg[reg_a], self.reg[reg_b]
            ans = 0
            while y > 0:
                if y & 1:
                    ans = ans + x
                x = x << 1
                y = y >> 1
            print(ans)

        elif op == 'CMP':
            # this instruction is used for comparison in values in other
            # instructions
            x, y = self.reg[reg_a], self.reg[reg_b]
            if x == y:
                self.FL = 1
            else:
                self.FL = 0
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,

            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        op_codes = {
            0b10000010: 'LDI',
            0b01000111: 'PRN',
            0b00000001: 'HLT',
            0b10100000: 'ADD',
            0b10100010: 'MUL',
            0b01000101: 'PUSH',
            0b01000110: 'POP',
            0b01010000: 'CALL',
            0b00010001: 'RET',
            0b00010001: 'RET',
            0b10100111: 'CMP',  # uses flags for comparisons in other inst
            0b01010100: 'JMP',  # jumps to the address in the given register
            0b01010101: 'JEQ',  # if E fl==1 jmp to address in given register
            0b01010110: 'JNE'   # if E fl==0 jmp to address in given register
            }
        alu_codes = set(['ADD', 'SUB', 'MUL', 'CMP'])
