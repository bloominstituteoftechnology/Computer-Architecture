"""CPU functionality."""

import sys


# Step 1: Add the constructor to cpu.py
# x = [0] * 25  # x is a list of 25 zeroes
# 256 bytes in total


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # RAM
        self.ram = [0] * 256
        # Our registers
        self.registers = [0] * 8  # 8 general-purpose registers, like variables, R0, R1, R2 .. R7
        # internal registers
        self.pc = 0  # Program Counter, index of the current instruction
        self.halted = False
        self.ir = 0
        # self.branch_table = {
        self.ldi = 0b10000010,
        self.prn = 0b01000111,
        # ADD: self.alu,
        # DIV: self.alu,
        # SUB: self.alu,
        # AND: self.alu,
        # OR: self.alu
        # }


# Step 2: Add RAM functions
# ram_read() should accept the address to read and return the value stored there.

# ram_write() should accept a value to write, and the address to write it to.


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""

        # path = 'examples/' + filename
        # address = 0
        # -- Load program ---
        with open(filename, 'r') as f:
            # for address, line in enumerate(f):
            for line in f:
                line = line.split('#')
                line = line[0].strip()
                # except ValueError:
                continue

                self.ram[address] = int(line, 2)
                address += 1

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

            # for address, instruction in enumerate(program):
            #     self.ram[address] = instruction
            #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == DIV:
            self.reg[reg_a] //= self.reg[reg_b]
        elif op == AND:
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == OR:
            self.reg[reg_a] |= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

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


# Step 3: Implement the core of CPU's run() method
# Step 4: Implement the HLT instruction handler
# Step 5: Add the LDI instruction
# Step 6: Add the PRN instruction
# Step 7: Un-hardcode the machine code
# Step 8: Implement a Multiply and Print the Result
# Step 9: Beautify your run() loop
# Step 10: Implement System Stack
# Step 11: Implement Subroutine Calls

        HLT = 0b00000001  # Instruction handler
        LDI = 0b10000010  # instruction
        PRN = 0b01000111  # PRN instruction

        ADD = 0b10100000
        SUB = 0b10100001
        MUL = 0b10100010
        DIV = 0b10100011

        AND = 0b10101000
        OR = 0b10101010

        running = True

        self.ir = self.ram_read(self.pc)
        reg_num1 = self.ram_read(self.pc + 1)  # register
        reg_num2 = self.ram_read(self.pc + 2)  # value

        while running:
            # Lets set our value of our register
            if self.ir == LDI:
                self.reg[reg_num1] = reg_num2
                self.pc += 3
            # print
            elif self.ir == PRN:
                print(self.reg[reg_num1])  # print our stored value
                self.pc += 2
                # Halt our CPU and exit
            elif self.ir == HLT:
                running = False
                self.pc += 1

            else:
                print(f"Unknown instruction {ir} at address {pc}")

                sys.exit(1)
