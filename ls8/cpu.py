"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.flag = 0b00000000

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""
        address = 0

        if len(sys.argv) != 2:
            print("usage: ls8.py progname")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    if line == '' or line[0] == "#":
                        continue

                    try:
                        str_value = line.split("#")[0]
                        value = int(str_value, 2)
                
                    except ValueError:
                        print(f"Invalid Number: {str_value}")
                        sys.exit(1)
                
                    self.ram[address] = value
                    address += 1
        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "CMP":
            first = self.reg[reg_a]
            second = self.reg[reg_b]
            if first == second:
                self.flag = 0b00000001
            elif first < second:
                self.flag = 0b00000100
            elif first > second:
                self.flag = 0b00000010
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
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        ADD = 0b10100000
        SUB = 0b10100001
        DIV = 0b10100011
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        SP = 7
        isRunning = True

        while isRunning:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                isRunning = False
                self.pc = 0
            elif ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == PRN:
                print(int(self.reg[operand_a]))
                self.pc += 2
            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif ir == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            elif ir == SUB:
                self.alu("SUB", operand_a, operand_b)
                self.pc += 3
            elif ir == DIV:
                self.alu("DIV", operand_a, operand_b)
                self.pc += 3
            elif ir == PUSH:
                SP -= 1
                self.ram_write(self.reg[operand_a], SP)
                self.pc += 2
            elif ir == POP:
                self.reg[operand_a] = self.ram[SP]
                SP += 1
                self.pc += 2
            elif ir == CALL:
                return_address = self.pc + 2
                SP -= 1
                self.ram_write(return_address, SP)
                self.pc = self.reg[operand_a]
            elif ir == RET:
                self.pc = self.ram[SP]
                SP += 1
            elif ir == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3
            elif ir == JMP:
                self.pc = self.reg[operand_a]
            elif ir == JEQ:
                if self.flag == 0b00000001:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif ir == JNE:
                if self.flag != 0b00000001:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            

