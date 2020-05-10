"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        # 8 new registers
        self.reg = [0] * 8
        # memory storage for ram
        self.ram = [0] * 256

    # accepts address to read and returns value stored
    def ram_read(self, mar):
        # mar contains address that is being read or written to
        return self.ram[mar]

    # accepts value to write, and address to write it to
    def ram_write(self, mdr, mar):
        # contains date that was read or written or data to write
        self.ram[mar] = mdr

    def load(self, prog):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        with open(prog) as program:
            for instruction in program:
                instruction_split = instruction.split('#')
                instruction_stripped = instruction_split[0].strip()

                if instruction_stripped == '':
                    continue
                instruction_num = int(instruction_stripped, 2)
                self.ram_write(instruction_num, address)
                address += 1

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
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        running = True

        while running:
            instruction = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            if instruction == HLT:
                running = False
                self.pc += 1
                sys.exit()
            elif instruction == LDI:
                self.reg[reg_a] = reg_b
                self.pc += 3
            elif instruction == PRN:
                print(self.reg[reg_a])
                self.pc += 2
            elif instruction == MUL:
                print(self.reg[reg_a] * self.reg[reg_b])
                self.pc += 3
            else:
                print(f'this instruction is not valid: {hex(instruction)}')
                running = False
                sys.exit()
