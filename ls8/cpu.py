"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.PC = 0
        self.SP = 7

    def ram_read(self, MAR):
        MDR = self.ram[MAR]
        return MDR

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, program):
        try:
            address = 0
            with open(program) as file:
                for line in file:
                    split_line = line.split('#')[0]
                    command = split_line.strip()

                    if command == '':
                        continue

                    instruction = int(command, 2)
                    self.ram_write(address, instruction)

                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            # self.fl,
            # self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def prn(self, operand_a):
        print(operand_a)

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        ADD = 0b10100000
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001

        running = True
        while running:
            IR = self.ram_read(self.PC)
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            if IR == LDI:
                self.ldi(operand_a, operand_b)
                self.PC += 3

            if IR == PRN:
                self.prn(self.reg[operand_a])
                self.PC += 2

            if IR == HLT:
                running = False

            if IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.PC += 3

            if IR == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.PC += 3

            if IR == PUSH:
                # decrement the stack pointer
                self.reg[self.SP] -= 1

                # get the register number
                reg_number = self.ram[self.PC + 1]
                # get a value from the given register
                value = self.reg[reg_number]

                # put the value at the stack pointer address
                sp = self.reg[self.SP]
                self.ram[sp] = value

                self.PC += 2

            if IR == POP:
                # get the stack pointer (where do we look?)
                sp = self.reg[self.SP]

                # get register number to put value in
                reg_number = self.ram[self.PC + 1]

                # use stack pointer to get the value
                value = self.ram_read(sp)
                # put the value into the given register
                self.reg[reg_number] = value
                # increment our stack pointer
                self.reg[self.SP] += 1

                # increment our program counter
                self.PC += 2

            if IR == CALL:
                # decrement the stack pointer
                self.reg[self.SP] -= 1

                # store return address in ram
                return_address = self.PC + 2
                self.ram[self.reg[self.SP]] = return_address

                # go to subroutine address
                subroutine_reg = self.PC + 1
                subroutine_address = self.ram[subroutine_reg]
                self.PC = self.reg[subroutine_address]

            if IR == RET:
                return_address = self.ram[self.reg[self.SP]]
                self.reg[self.SP] += 1
                self.PC = return_address
