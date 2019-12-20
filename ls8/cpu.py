"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0 
        self.registers = [0] * 8
        # self.ram =[[0] * 8] * 256 #256 bytes of ram
        self.SP = 7
        self.ram = [0] * 256
        self.FL = 0b11111111

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
            reg_a += reg_b
            return reg_a
        #elif op == "SUB": etc
        elif op == "MUL":
            return reg_a * reg_b
        elif op == "CMP":
            print(f"A {reg_a}, B {reg_b}, Flag {self.FL}")
            if reg_a is reg_b:
                self.FL = (self.FL & 0b00000001)
            elif reg_a > reg_b:
                self.FL = (self.FL & 0b00000010)
            elif reg_a < reg_b:
                self.FL = (self.FL & 0b00000100)
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

    def jump(self, reg):
        self.pc = reg

    def run(self):
        """Run the CPU."""
        running = True
        # SP = 5

        
        LDI = 0b10000010
        HALT = 0b00000001
        PRN = 0b01000111
        MUL = 0b10100010
        ADD = 0b10100000
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        #ir


        while running:
            instruction_register = self.ram_read(self.pc)
            # incr = ((instruction_register & 0b11111111) >> 6) + 1
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # print("Current instruction", instruction_register)
            # print("in", instruction_register)
            if instruction_register == LDI:
                print("store", operand_a, operand_b)
                self.registers[operand_a] = operand_b
                self.pc += 3
                # self.pc += incr

            elif instruction_register == PRN:
                # print("print", operand_a)
                print(self.registers[operand_a])
                self.pc += 2
                # self.pc += incr
            elif instruction_register == ADD:
                print(self.alu("ADD", self.registers[operand_a], self.registers[operand_b]))
                self.pc += 3
            elif instruction_register == MUL:
                print(self.alu("MUL", self.registers[operand_a], self.registers[operand_b]))
                # print(self.registers[operand_a] * self.registers[operand_b])
                # self.pc += 3
                self.pc += 3
            elif instruction_register == JEQ:
                if self.FL == (self.FL & 0b00000001):
                    self.jump(self.registers[operand_a])
            elif instruction_register == JMP:
                self.jump(self.registers[operand_a])
            elif instruction_register == CMP:
                print("CMP")
                self.alu("CMP",self.registers[operand_a], self.registers[operand_b])
                print(self.FL)
            elif instruction_register == PUSH:
                # decrement the stack pointer
                # SP -= 1
                self.registers[self.SP]-=1
                # self.SP -= 1
                reg_num = self.ram[self.pc + 1]
                value = self.registers[reg_num]
                self.ram[self.registers[self.SP]] = value
                # reg_num = self.ram[self.pc + 1]
                # reg_val = self.registers[reg_num]
                # self.ram[self.registers[self.SP]] =reg_val
                # self.ram_write(self.registers[self.SP], self.registers[reg_val])
                print("PUSH", value, reg_num, "address", self.ram[self.registers[self.SP]], self.registers[self.SP], "pointer", self.SP)
                self.pc+=2
                # self.registers[self.SP] -= 1
                # self.pc += 1
                # # copy value from register to memory at stack pointer
                # reg_num = self.ram[self.pc]
                # # print("Reg_num", reg_num)
                # value = self.registers[reg_num]
                # self.ram[self.registers[self.SP]] = value

                # self.pc += 2
            elif instruction_register == POP:
                # copy the value from the top of the stack into a given register
                # self.pc += 1
                # reg_val = self.ram_read(self.registers[self.SP])
                reg_val = self.ram[self.registers[self.SP]]

                # reg_num = self.ram_read(self.pc + 1)
                reg_num = self.ram[self.pc + 1]
                self.registers[reg_num] = reg_val
                self.registers[self.SP] += 1
                self.pc += 2

                # self.pc += 1
                # reg_num = self.ram[self.pc]
                # value = self.ram[self.registers[self.SP]]
                # self.registers[reg_num] = value
                # # increment
                # self.SP += 1
                # print("POP", SP, "Value:", value, "new sp:", SP)
                # self.registers[SP]
            elif instruction_register == CALL:
                print("Call")
                return_address = self.pc + 2
                self.registers[self.SP] -= 1
                self.ram[self.registers[self.SP]] = return_address

                reg_num = self.ram[self.pc + 1]
                sub_address = self.registers[reg_num]
                self.pc = reg_num
            elif instruction_register == RET:
                self.pc = self.registers[self.SP]
            elif instruction_register == HALT:
                running = False
                # self.pc += 1
            else:
                print("Nope")
                sys.exit()
                # self.pc += 1
                # self.pc += incr
