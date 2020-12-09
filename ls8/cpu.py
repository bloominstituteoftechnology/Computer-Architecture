"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[7] = 0xf4
        self.running = False
        self.branchTable = {
            130: self.ldi,
            71: self.prn,
            162: self.mult,
            1: self.halt,
            69: self.pushy,
            70: self.poppy
        }

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

    def ldi(self, op_a, op_b):
        self.reg[op_a] = op_b
        self.pc += 3

    def prn(self, op_a, op_b):
        print("Printing", self.reg[op_a])
        self.pc += 2

    def halt(self, op_a, op_b):
        print("Halt")
        self.running = False

    def mult(self, op_a, op_b):
        print("alu", self.alu("MUL", op_a, op_b))

    def pushy(self, op_a, op_b):
        self.reg[7] -= 1
        register_address = self.ram[self.pc + 1]
        value = self.reg[register_address]
        self.ram[self.reg[7]] = value
        self.pc += 2

    def poppy(self, op_a, op_b):
        value = self.ram[self.reg[7]]
        register_address = self.ram[self.pc + 1]
        self.reg[register_address] = value
        self.reg[7] += 1
        self.pc += 2

    def run(self):
        self.running = True

        while self.running:
            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            try:
                self.branchTable[instruction](operand_a, operand_b)

            except Exception:
                print(
                    f'Could not find that particular instruction.{instruction}')

    # def run(self):
    #     ldi = 130
    #     prn = 71
    #     mul = 162
    #     hlt = 1
    #     """Run the CPU."""
    #     self.running = True

    #     while self.running:
    #         instruction = self.ram_read(self.pc)
    #         operand_a = self.ram_read(self.pc+1)
    #         operand_b = self.ram_read(self.pc+2)
    #         if instruction == ldi:
    #             self.reg[operand_a] = operand_b
    #             self.pc += 3
    #             print("first loop")
    #         elif instruction == prn:
    #             print("Printing", self.reg[operand_a])
    #             self.pc += 2
    #         elif instruction == hlt:
    #             print("Halt")
    #             self.running = False
    #         elif instruction == mul:
    #             print("alu", self.alu("MUL", operand_a, operand_b))
    #         else:
    #             print(
    #                 f'Could not find that particular instruction.{instruction}')

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
