"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        # General Purpose Registers
        self.registers = [0] * 8

        # Stack Pointer
        self.sp = 7
        self.registers[7] = 0xF4

        # Internal Registers
        self.pc = 0
        self.ir = 0
        # self.mar = 0
        # self.mdr = 0
        self.fl = 0b00000000

        # Instructions
        self.CALL = 0b01010000
        self.RET = 0b00010001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010
        self.ADD = 0b10100000
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.CMP = 0b10100111
        self.JMP = 0b01010100
        self.JEQ = 0b01010101
        self.JNE = 0b01010110

        # RAM
        self.ram = [0] * 256

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        program = []

        with open(sys.argv[1]) as f:
            program = [line.strip('\n') for line in f]

        program = [int(i[:8], 2) for i in program if len(i) > 1 if i[0] != '#']

        # print(program)

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == self.ADD:
            return self.registers[reg_a] + self.registers[reg_b]
        #elif op == "SUB": etc
        elif op == self.MUL:
            return self.registers[reg_a] * self.registers[reg_b]
        elif op == self.CMP:
            if self.registers[reg_a] == self.registers[reg_b]:
                self.fl = 0b00000001
            # elif self.registers[reg_a] < self.registers[reg_b]:
            #     self.fl = 0b00000100
            # elif self.registers[reg_a] > self.registers[reg_b]:
            #     self.fl = 0b00000010
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def ram_read(self, read_value):
        return self.ram[read_value]

    def ram_write(self, write_value, write_address_location):
        self.ram[write_address_location] = write_value

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            instruction = self.ram[self.pc]

            if instruction == self.LDI:
                MAR = self.ram[self.pc + 1]
                MDR = self.ram[self.pc + 2]

                self.registers[MAR] = MDR

                self.pc += 2

            elif instruction == self.PUSH:
                self.registers[self.sp] -= 1

                reg = self.ram[self.pc + 1]
                value  = self.registers[reg]

                self.ram_write(value, self.registers[self.sp])

                self.pc += 1

            elif instruction == self.POP:
                value = self.ram_read(self.registers[self.sp])
                
                reg = self.ram[self.pc + 1]
                self.registers[reg] = value

                self.registers[self.sp] += 1

                self.pc += 1

            elif instruction == self.CALL:
                self.registers[self.sp] -= 1
                
                reg = self.ram[self.pc + 1]
                pc_value  = self.registers[reg]

                self.ram_write(self.pc + 2, self.registers[self.sp])

                self.pc = pc_value

            elif instruction == self.RET:
                value = self.ram_read(self.registers[self.sp])
                self.pc = value

                self.registers[self.sp] += 1

            elif instruction == self.JMP:
                self.pc = self.registers[self.ram_read(self.pc + 1)]

            elif instruction == self.JEQ:
                if self.fl == 0b00000001:
                    self.pc = self.registers[self.ram_read(self.pc + 1)]
                else:
                    self.pc += 2

            elif instruction == self.JNE:
                if self.fl == 0b00000000:
                    self.pc = self.registers[self.ram_read(self.pc + 1)]
                else:
                    self.pc += 2

            elif instruction == self.MUL:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]

                MAR = reg_a
                MDR = self.alu(instruction, reg_a, reg_b)

                self.registers[MAR] = MDR

                self.pc += 2

            elif instruction == self.ADD:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]

                MAR = reg_a
                MDR = self.alu(instruction, reg_a, reg_b)

                self.registers[MAR] = MDR

                self.pc += 2

            elif instruction == self.CMP:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]

                self.alu(instruction, reg_a, reg_b)

                self.pc += 2

            elif instruction == self.PRN:
                print(self.registers[self.ram[self.pc + 1]])

                self.pc += 1

            elif instruction == self.HLT:
                print("Exiting program.")
                running = False

            else:
                print(instruction)
                print("Unknown Instruction. Exiting Program.")
                running = False

            if instruction not in [self.CALL, self.RET, self.JMP, self.JNE, self.JEQ]: 
                self.pc += 1
