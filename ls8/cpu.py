"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        try:
            if len(sys.argv) < 2:
                print(f'Error from {sys.argv[0]}): missing file name argument')
                sys.exit(1)

            with open(sys.argv[1]) as f:
                for line in f:
                    split_line = line.split("#")[0]
                    stripped_line = split_line.strip()
                    # print(int(stripped_line, 2))
                    if stripped_line != "":
                        command = int(stripped_line, 2)
                        print(command)
                        self.ram[address] = command
                        address += 1
        except FileNotFoundError:
            print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
            print("(Did you double check the file name?)")
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
            self.pc += 2
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
            self.pc += 2
        elif op == 'MUL':
            print("multiply")
            result = self.reg[reg_a] * self.reg[reg_b]
            self.pc += 2
            return result
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
        ldi = 130
        prn = 71
        mul = 162
        hlt = 1
        """Run the CPU."""
        self.running = True
        # IR = {}
        # IR[self.pc] = self.reg[self.pc]

        while self.running:
            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            if instruction == ldi:
                self.reg[operand_a] = operand_b
                self.pc += 3
                print("first loop")
            elif instruction == prn:
                print("Printing", self.reg[operand_a])
                self.pc += 2
            elif instruction == hlt:
                print("Halt")
                self.running = False
            elif instruction == mul:
                print("alu", self.alu("MUL", operand_a, operand_b))
            else:
                print(
                    f'Could not find that particular instruction.{instruction}')
                return

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
