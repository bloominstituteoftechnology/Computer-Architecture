"""CPU functionality."""

import sys

program_file = "6. Architecture/Computer-Architecture/ls8/examples/print8.ls8"

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0 
        self.running = True

    def load(self):
        """Load a program into memory."""
        # print(f"SYS.ARGV: {sys.argv}")

        # if len(sys.argv) != 2:
        #     print("usage: 02_fileio2.py filename")

        address = 0

        try:
            with open(progra
            m_file) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == "":
                        continue

                    x = int(n, 2)
                    print(f"{x:08b}: {x:d}")
                    self.ram[address] = x
                    address += 1

        except:
            print(f"{sys.argv[0]} / {sys.argv[1]} not found")


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
        
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
        ADD  = 0b10100000
        PUSH = 0b01000101
        POP = 0b01000110


        while self.running:
            IR = self.ram[self.pc]
            print(f"Bad imput: {IR}")
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == HLT:
                self.running = False
                self.pc += 1
            elif IR == LDI:
                self.reg[operand_a] = operand_b
                print(operand_a)
                self.pc += 3   
            elif IR == PRN:
                print(operand_a)
                self.pc += 2
            elif IR == MUL:
                res = self.reg[operand_a] * self.reg[operand_b]
                print(res)
                self.pc += 3
            elif IR == ADD:
                res = self.reg[operand_a] + self.reg[operand_b]
                print(res)
            elif IR == PUSH:
                self.reg[7] -= 1
                sp = self.reg[7]

                value = self.reg[operand_a]
                self.ram[sp] = value

                self.pc += 2
            elif IR == POP:
                sp = self.reg[7]

                value = self.ram[sp]
                self.reg[operand_a] = value

                self.reg[7] += 1                
                self.pc += 2
            else:
                self.running = False
                print(f"Bad imput: {IR}")        
            
        
cpu = CPU()
cpu.load()
cpu.run()