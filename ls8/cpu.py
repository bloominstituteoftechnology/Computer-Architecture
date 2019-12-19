"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0 
        self.registers = [0] * 8
        self.ram =[[0] * 8] * 256 #256 bytes of ram
        # self.SP = self.registers[7]

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        filename = sys.argv[1]

        with open(filename) as f:
            for line in f:
                n = line.split("#")
                n[0] = n[0].strip()

                if n[0] == "":
                    continue
                val = int(n[0], 2)
                self.ram[address] = val
                address += 1


        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, MAR):
        value = self.ram[MAR]

        return value

    def ram_write(self, MAR, MAD):
        # register_number = self.ram[self.pc + 1]
        # value = self.ram[self.pc + 2]
        self.ram[MAR] = MAD

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
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        SP = 7

        
        LDI = 0b10000010
        HALT = 0b00000001
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        #ir


        while running:
            instruction_register = self.ram_read(self.pc)
            incr = ((instruction_register & 0b11111111) >> 6) + 1
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if instruction_register == LDI:
                print("store", operand_a, operand_b)
                self.registers[operand_a] = operand_b
                # self.pc += 3
            elif instruction_register == PRN:
                print("print", operand_a)
                print(self.registers[operand_a])
                # self.pc += 2
            elif instruction_register == MUL:
                print(self.registers[operand_a] * self.registers[operand_b])
                # self.pc += 3
            elif instruction_register == PUSH:
                # decrement the stack pointer
                self.registers[SP] -= 1
                # copy value from register to memory at stack pointer
                reg_num = self.ram[self.pc + 1]
                value = self.registers[reg_num]
                self.ram[self.registers[SP]] = value

                self.pc += 2
            elif instruction_register == POP:
                # copy the value from the top of the stack into a given register
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.registers[SP]]
                self.registers[reg_num] = value
                # iuncrement
                self.registers[SP]
                self.pc += 2
            elif instruction_register == HALT:
                running = False
                # self.pc += 1
            else:
                print("Nope")
            self.pc += incr
