"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self, filename):
        """Construct a new CPU."""
        self.reg = [0] * 256
        self.ram = [0] * 128
        self.filename = filename
        self.stack_pointer = 0xF4
        self.flags = [0] * 8
    def load(self):
        """Load a program into memory."""

        address = 0

        with open(self.filename, 'r') as f:
            program = f.read().splitlines()
            program = ['0b'+line[:8] for line in program if line and line[0] in ['0', '1']]


        for instruction in program:
            self.ram[address] = eval(instruction)
            address += 1

        # print(self.ram)
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            self.flags = [0] * 8
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flags[5] = 1
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.flags[6] = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flags[7] = 1
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print("RAM:", self.ram)
        print("REG:", self.reg[:10])
        print("STACK:", self.reg[self.stack_pointer:0xF4])

    def run(self):
        """Run the CPU."""

        address = 0
        while True:
            instruction = self.ram[address]
            # LDI
            if instruction == 0b10000010:
                register = self.ram[address + 1]
                integer = self.ram[address + 2]
                address += 3
                self.reg[register] = integer
            # PRN
            elif instruction == 0b01000111:
                register = self.ram[address + 1]
                address += 2
                print(self.reg[register])
            # ADD
            elif instruction == 0b10100000:
                self.alu("ADD", self.ram[address + 1], self.ram[address + 2])
                address += 3
            # MUL
            elif instruction == 0b10100010:
                self.alu("MUL", self.ram[address + 1], self.ram[address + 2])
                address += 3
            # PUSH
            elif instruction == 0b01000101:
                register = self.ram[address + 1]
                self.stack_pointer -= 1
                self.reg[self.stack_pointer] = self.reg[register]
                address += 2
            # POP
            elif instruction == 0b01000110:
                register = self.ram[address + 1]
                self.reg[register] = self.reg[self.stack_pointer]
                self.stack_pointer += 1
                address += 2
            # CALL
            elif instruction == 0b01010000:
                self.stack_pointer -= 1
                self.reg[self.stack_pointer] = address + 2
                address = self.reg[self.ram[address + 1]]
            # RET
            elif instruction == 0b00010001:
                address = self.reg[self.stack_pointer]
                self.stack_pointer += 1
            # CMP
            elif instruction == 0b10100111:
                self.alu("CMP", self.ram[address + 1], self.ram[address + 2])
                address += 3
            # JMP
            elif instruction == 0b01010100:
                address = self.reg[self.ram[address + 1]]
            # JEQ
            elif instruction == 0b01010101:
                if self.flags[6] == 1:
                    address = self.reg[self.ram[address + 1]]
                else:
                    address += 2
            # JNE
            elif instruction == 0b01010110:
                if self.flags[6] != 1:
                    address = self.reg[self.ram[address + 1]]
                else:
                    address += 2

            # HLT
            elif instruction == 0b00000001:
                break






            else:
                # print(address, 'address')
                # print(instruction)
                raise TypeError("That command has not been implemented yet")
