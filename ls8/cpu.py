"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0 # not a command
        self.HLT = 1 # command
        self.LDI = 130 # command
        self.PRN = 71 # command
        self.PUSH = 69 # command
        self.POP = 70 # command
        self.MUL = 162 # command
        self.sp = 7 # not a command
        self.CMP = 167
        self.JMP = 84
        self.JEQ = 85
        self.JNE = 86
        self.fl = 0

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) != 2:
            print("usage: ls8.py filename")
            sys.exit(1)

        try:

            address = 0

            with open(sys.argv[1]) as f:
                for line in f:
                    t = line.split('#')
                    n = t[0].strip()

                    if n == '':
                        continue

                    try:
                        n = int(n, 2)
                    except ValueError:
                        print(f"Invalid number: '{n}")
                        sys.exit(1)

                    self.ram_write(address, n)
                    address += 1

        except FileNotFoundError:
            print(f'File not found: {sys.argv[1]}')
            sys.exit(2)




    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] //= self.reg[reg_b]
        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]
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

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            ir = self.ram_read(self.pc)
            if ir == self.LDI:
                self.pc += 1
                reg_idx = self.ram_read(self.pc)
                self.pc += 1
                reg_val = self.ram_read(self.pc)
                self.reg[reg_idx] = reg_val
                self.pc += 1
            elif ir == self.MUL:
                self.pc += 1
                num1_idx = self.ram_read(self.pc)
                self.pc += 1
                num2_idx = self.ram_read(self.pc)
                self.alu("MUL", num1_idx, num2_idx)
                self.pc += 1
            elif ir == self.PUSH:
                self.pc += 1
                reg_num = self.ram[self.pc]
                value = self.reg[reg_num]
                stack_top = self.reg[self.sp]
                self.ram[stack_top] = value
                self.pc += 1
            elif ir == self.POP:
                self.pc += 1
                reg_num = self.ram[self.pc]
                stack_top = self.reg[self.sp]
                value = self.ram[stack_top]
                self.reg[reg_num] = value
                self.reg[self.sp] += 1
                self.pc += 1
            elif ir == self.PRN:
                self.pc += 1
                print(self.reg[self.ram_read(self.pc)])
                self.pc += 1
            elif ir == self.CMP:
                self.pc += 1
                registerA = self.reg[self.ram_read(self.pc)]
                self.pc += 1
                registerB = self.reg[self.ram_read(self.pc)]
                if registerA < registerB:
                    self.fl = 4
                elif registerA > registerB:
                    self.fl = 2
                elif registerA == registerB:
                    self.fl = 1
                self.pc += 1
            elif ir == self.JEQ:
                if self.fl == 1:
                    self.pc = self.reg[self.ram_read(self.pc)]
            elif ir == self.HLT:
                running = False