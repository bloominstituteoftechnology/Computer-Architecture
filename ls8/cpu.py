"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0b0] * 256
        self.registers = [0] * 8
        self.registers[7] = 0xF4

        self.PC = 0
        self.IR = self.ram[self.PC]
        self.FL = 0

        self.pointer = 7

        self.operations = {
            'HLT': 0b00000001,
            'LDI': 0b10000010,
            'PRN': 0b01000111,
            'MUL': 0b10100010,
            'ADD': 0b10100000,
            'PUSH': 0b01000101,
            'POP': 0b01000110,
            'CALL': 0b01010000,
            'RET': 0b00010001,
            'NOP': 0b00000000
        }

    def load(self, program=None):
        """Load a program into memory."""
        address = 0
        if program:
            with open(program) as f:
                for line in f:
                    x = line.split('#')[0].strip()
                    if x is '':
                        continue

                    else:
                        instruction = int(x, 2)
                        self.ram[address] = instruction
                        address += 1

        else:
            # For now, we've just hardcoded a program:

            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]

            for instruction in program:
                self.ram[address] = instruction
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        active = True

        while active is True:
            self.IR = self.ram_read(self.PC)

            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            if self.IR == self.operations['HLT']:
                active = False

            elif self.IR == self.operations['LDI']:
                self.registers[operand_a] = operand_b
                self.PC += 3

            elif self.IR == self.operations['PRN']:
                print(self.registers[operand_a])
                self.PC += 2

            elif self.IR == self.operations['MUL']:
                self.alu('MUL', operand_a, operand_b)
                self.PC += 3

            elif self.IR == self.operations['ADD']:
                self.alu('ADD', operand_a, operand_b)
                self.PC += 3

            elif self.IR == self.operations['PUSH']:
                self.registers[self.pointer] -= 1
                self.ram_write(self.registers[operand_a],
                               self.registers[self.pointer])
                self.PC += 2

            elif self.IR == self.operations['POP']:
                x = self.ram_read(self.registers[self.pointer])
                self.registers[operand_a] = x
                self.registers[self.pointer] += 1
                self.PC += 2

            elif self.IR == self.operations['CALL']:
                self.registers[self.pointer] -= 1
                self.ram_write(self.PC + 2, self.registers[self.pointer])
                self.PC = self.registers[operand_a]

            elif self.IR == self.operations['RET']:
                self.PC = self.ram_read(self.registers[self.pointer])

            elif self.IR == self.operations['NOP']:
                self.PC += 1
                continue

            else:
                print(f'ERROR: UNKNOWN INSTRUCTION {self.IR} @ {self.PC}')
                self.PC += 1

    def ram_read(self, register):
        return self.ram[register]

    def ram_write(self, data, register):
        self.ram[register] = data


if __name__ == "__main__":
    LS8 = CPU()
    LS8.load('examples/stack.ls8')
    LS8.run()
