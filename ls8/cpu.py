"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        # register1, register2, register3, register4, register5, register6, register7, register8 = (self.ram for i in range(8))
        # print(register1, register2, register3, register4, register5, register6, register7, register8)
        self.reg = [0] * 8
        self.pc = 0
        self.IR = 0
        self.reg[7] = 0xf4
        self.SP = 7
        self.E = 0
        self.L = 0
        self.G = 0
        self.live = True
        # pass

    def ram_read(self, address):
        return self.ram[address]        

    def ram_write(self, address, value):
        self.ram[address] = value

    def push(self, a):
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.reg[a]
    
    def pop(self, a):
        self.reg[a] = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1

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
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        with open(sys.argv[1]) as f:
            for line in f:
                if line[0] != '#' and line != '\n':
                    self.ram[address] = int(line[0:8], 2)
                    address += 1
            f.closed
        # print(self.ram)
        # print(self.reg)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'CMP':
            if self.reg[reg_a] == self.reg[reg_b]:
                self.E = 1
                self.L = 0
                self.G = 0
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.E = 0
                self.L = 1
                self.G = 0
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.E = 0
                self.L = 0
                self.G = 1
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
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # live = True
        # IR = self.ram[self.PC]

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        POP = 0b01000110
        PUSH = 0b01000101
        CMP = 0b10100111
        CALL = 0b01010000
        RET = 0b00010001
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110
        
        while self.live:
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # print(self.PC)
            if self.ram[self.pc] == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif self.ram[self.pc] == PRN:
                print(self.reg[operand_a])
                self.pc += 2

            elif self.ram[self.pc] == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3

            elif self.ram[self.pc] == PUSH:
                self.reg[self.SP] -= 1
                self.ram[self.reg[self.SP]] = self.reg[operand_a]
                self.pc += 2

            elif self.ram[self.pc] == POP:
                self.reg[operand_a] = self.ram[self.reg[self.SP]]
                self.reg[self.SP] += 1
                self.pc += 2

            elif self.ram[self.pc] == CALL:
                self.reg[4] = self.pc + 2
                self.push(4)
                self.pc = self.reg[operand_a]

            elif self.ram[self.pc] == RET:
                self.pop(0x04)
                self.pc = self.reg[0x04]

            elif self.ram[self.pc] == JMP:
                self.pc = self.reg[operand_a]

            elif self.ram[self.pc] == CMP:
                self.alu('CMP', operand_a, operand_b)
                self.pc += 3
                
            elif self.ram[self.pc] == JEQ:
                if self.E == 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            elif self.ram[self.pc] == JNE:
                if self.E == 0:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            elif self.ram[self.pc] == HLT:
                self.live == False
                break

            else:
                self.live = False
                break
                # print(f'{self.ram[self.pc]} is an invalid argument.')