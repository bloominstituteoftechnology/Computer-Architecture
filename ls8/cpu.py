"""CPU functionality."""

import sys
import os

HTL = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010


class CPU:
    def __init__(self):
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.fl = 0

    def write_program_to_memory(self, program_file):
        address = 0
        with open(os.path.join(sys.path[0], program_file), 'r') as file:
            for line in file:
                line_value = line.split()

                # if able to change into an integer with a binary value
                # add it to ram
                try:
                    binary_instruction = int(line_value[0], 2)

                    # add file to memory list
                    if address < 257:
                        self.ram[address] = binary_instruction
                        address += 1

                # if tried failed, continue to next line
                except:
                    continue
        if not file:
            print('no data in file')
            program = [HTL]

    def load(self):
        """Load a program into memory."""
        args = sys.argv

        if len(args) > 1:
            program_file = args[1]
            try:
                self.write_program_to_memory(program_file)
            except:
                print('Unexpected error: ', sys.exc_info()[0])
        else:
            print(
                'too few arguments, please choose a program to run: "python3 ls8.py examples/program_file.ls8"')

    def ram_read(self, MAR):
        '''
        Returns what is stored at the given address.
        '''
        if MAR < len(self.ram):
            return self.ram[MAR]
        else:
            raise IndexError

    def ram_write(self, MAR, MDR):
        '''
        Writes the given value to the address given.
        '''
        if MAR < len(self.ram):
            self.ram[MAR] = MDR
        else:
            raise IndexError

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]

        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ops(self, op, reg_a, reg_b):
        '''OPS operations.'''
        pass

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
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR is HTL:
                self.handle_halt()
            elif IR is LDI:
                self.handle_ldi(operand_a, operand_b)
                self.pc += 2
            elif IR is PRN:
                self.handle_print(operand_a)
                self.pc += 1
            elif IR is MUL:
                self.alu(IR, operand_a, operand_b)
                self.pc += 2

            self.pc += 1

    def handle_halt(self):
        # cpu reset
        # for i in range(0, 6):
        #     self.reg[i] = 0
        # self.reg[7], self.pc, self.fl, self.ram == 0xF4, 0, 0, [0] * 256

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
