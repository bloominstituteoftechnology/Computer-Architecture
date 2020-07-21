"""CPU functionality."""

import sys

HTL = 0b00000001
LDI = 0b10000010
PRN = 0b01000111


class CPU:
    def __init__(self):
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.fl = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

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

        while True:
            instruction = bin(self.ram_read(self.pc))

            print('instruction: ', instruction[2:])

            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR is HTL:
                self.handle_halt()
            elif IR is LDI:
                self.handle_ldi(operand_a, operand_b)
            elif IR is PRN:
                self.handle_print(operand_a)

            self.pc += 1

    def handle_halt(self):
        # cpu reset
        for i in range(0, 6):
            self.reg[i] = 0
        self.reg[7], self.pc, self.fl, self.ram == 0xF4, 0, 0, 0

        sys.exit(1)

    def handle_print(self, index):
        '''
        print numeric value stored at given register
        '''
        print(self.reg[index])

    def handle_ldi(self, register_index, value):
        '''
        set the value of a register to an integer
        '''
        if register_index < len(self.reg):
            self.reg[register_index] = value
        else:
            raise IndexError

    def ram_read(self, MAR):
        '''
        Returns what is stored at the given address.
        '''
        try:
            if MAR < len(self.ram):
                return self.ram[MAR]
        except IndexError:
            return f'address is out of range.'

    def ram_write(self, MAR, MDR):
        '''
        Writes the given value to the address given.
        '''
        try:
            if MAR < len(self.ram):
                self.ram[MAR] = MDR
        except IndexError:
            return f'address is out of range.'